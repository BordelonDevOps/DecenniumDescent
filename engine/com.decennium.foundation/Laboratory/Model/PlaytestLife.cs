#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using System.Linq;

namespace Decennium.Foundation.Laboratory
{
    public enum Injury { None = 0, Concussion = 1, OffensiveTrauma = 2, MobilityTrauma = 3,
        FineMotorTrauma = 4, ExertionTrauma = 5, CognitiveTrauma = 6 }

    /// <summary>Immutable normal/temp HP and linked Wounds. Other condition causes are separate.</summary>
    public sealed class LifeState
    {
        public long MaximumHp { get; }
        public long Hp { get; }
        public long TemporaryHp { get; }
        // One record per Wound; None means a Wound without a linked Injury.
        public IReadOnlyList<Injury> Wounds { get; }
        public bool Stable { get; }
        public bool Dead { get; }
        public bool UsesDeathSaves { get; }
        public int DeathSuccesses { get; }
        public int DeathFailures { get; }
        public long? StableUntilSeconds { get; }
        public long LastDeathTurn { get; }
        public bool Critical => Wounds.Count == 3;
        public long HealingCeiling => Critical ? Math.Max(1, MaximumHp - 1) : MaximumHp;

        public LifeState(long maximumHp, long hp, long temporaryHp = 0, IEnumerable<Injury> wounds = null,
            bool stable = false, bool dead = false, int deathSuccesses = 0, int deathFailures = 0,
            bool usesDeathSaves = true, long? stableUntilSeconds = null, long lastDeathTurn = 0)
        {
            if (maximumHp < 1 || hp < 0 || hp > maximumHp || temporaryHp < 0 || lastDeathTurn < 0)
                throw new ArgumentOutOfRangeException(nameof(hp), "Invalid life-state quantity.");
            Injury[] records = (wounds ?? Array.Empty<Injury>()).ToArray();
            if (records.Length > 3 || records.Any(x => x < Injury.None || x > Injury.CognitiveTrauma))
                throw new ArgumentException("At most three Wounds with valid linked injuries.", nameof(wounds));
            if (deathSuccesses < 0 || deathSuccesses > 3 || deathFailures < 0 || deathFailures > 3
                || (!dead && (deathSuccesses >= 3 || deathFailures >= 3))
                || ((hp > 0 || stable || !usesDeathSaves) && (deathSuccesses != 0 || deathFailures != 0)))
                throw new ArgumentException("Unresolved or incompatible death counters.");
            if (((dead || stable) && hp != 0) || (dead && stable))
                throw new ArgumentException("Dead and Stable are exclusive zero-HP states.");
            if (hp == 0 && !dead && !stable && !usesDeathSaves)
                throw new ArgumentException("An ordinary creature at zero HP must be Dead or legally Stable.");
            if (stableUntilSeconds < 0 || stable != stableUntilSeconds.HasValue)
                throw new ArgumentException("Stable requires its recorded recovery deadline; other states cannot retain one.");
            MaximumHp=maximumHp; Hp=hp; TemporaryHp=temporaryHp; Wounds=Array.AsReadOnly(records);
            Stable=stable; Dead=dead; DeathSuccesses=deathSuccesses; DeathFailures=deathFailures;
            UsesDeathSaves=usesDeathSaves; StableUntilSeconds=stableUntilSeconds; LastDeathTurn=lastDeathTurn;
        }
    }

    public sealed class DamageResolution
    {
        public LifeState State { get; }
        public long PostTempDamage { get; }
        public long TemporaryAbsorbed { get; }
        public long NormalHpLost { get; }
        public bool InstantDeath { get; }
        public int WoundSaves => WoundDc.HasValue ? 1 : 0;
        public long? WoundDc { get; }
        public long? WoundTotal { get; }
        public int InjuryRolls { get; }
        public int DeathFailuresAdded { get; }
        internal DamageResolution(LifeState state, long post, long absorbed, long lost, bool instant,
            long? dc, long? total, int injuries, int failures)
        { State=state; PostTempDamage=post; TemporaryAbsorbed=absorbed; NormalHpLost=lost;
          InstantDeath=instant; WoundDc=dc; WoundTotal=total; InjuryRolls=injuries; DeathFailuresAdded=failures; }
    }

    /// <summary>
    /// CORE_RESOLUTION_PLAYTEST damage/life procedure. Inputs are already legal post-defense events.
    /// No action/target legality, defense, survival replacement, condition dispatch or RNG selection.
    /// Declared rolls are required only when reached; failures never mutate the input.
    /// </summary>
    public static class PlaytestLife
    {
        private static void RequireState(LifeState state)
        { if (state == null) throw new ArgumentNullException(nameof(state)); }
        private static int Die(int? value, int sides, string label)
        {
            if (!value.HasValue || value.Value < 1 || value.Value > sides)
                throw new ArgumentException("A valid " + label + " is required.");
            return value.Value;
        }
        private static LifeState DeadState(LifeState s, long temp, int failures) => new LifeState(
            s.MaximumHp,0,temp,s.Wounds,dead:true,deathSuccesses:s.DeathSuccesses,
            deathFailures:failures,usesDeathSaves:s.UsesDeathSaves,lastDeathTurn:s.LastDeathTurn);

        public static LifeState Stabilize(LifeState state, int recoveryD4, long nowSeconds)
        {
            RequireState(state); Die(recoveryD4,4,"Stable recovery d4");
            if (nowSeconds < 0) throw new ArgumentOutOfRangeException(nameof(nowSeconds));
            if (state.Dead || state.Stable || state.Hp != 0)
                throw new ArgumentException("Only a living dying creature can stabilize.");
            long deadline=checked(nowSeconds + recoveryD4 * 3600L);
            return new LifeState(state.MaximumHp,0,state.TemporaryHp,state.Wounds,stable:true,
                usesDeathSaves:state.UsesDeathSaves,stableUntilSeconds:deadline,lastDeathTurn:state.LastDeathTurn);
        }

        public static LifeState Heal(LifeState state, long amount, bool hpRecoveryProhibited = false)
        {
            RequireState(state);
            if (amount < 0) throw new ArgumentOutOfRangeException(nameof(amount));
            if (state.Dead) throw new ArgumentException("Ordinary healing cannot restore the dead.");
            if (hpRecoveryProhibited) return state;
            long gained=Math.Min(amount,Math.Max(0,state.HealingCeiling-state.Hp));
            if (gained == 0) return state;
            return new LifeState(state.MaximumHp,state.Hp+gained,state.TemporaryHp,state.Wounds,
                usesDeathSaves:state.UsesDeathSaves,lastDeathTurn:state.LastDeathTurn);
        }

        public static DamageResolution Damage(LifeState state, long resolvedDamage, int constitutionSaveModifier = 0,
            int? woundNatural = null, int? injuryD6 = null, bool critical = false, bool maiming = false,
            bool knockout = false, bool melee = false, int? stableD4 = null, long nowSeconds = 0)
        {
            RequireState(state);
            if (resolvedDamage < 0 || nowSeconds < 0) throw new ArgumentOutOfRangeException(nameof(resolvedDamage));
            if (state.Dead) throw new ArgumentException("Dead target is outside living-damage handling.");
            if (knockout && !melee) throw new ArgumentException("Knockout requires a melee attack.");
            long absorbed=Math.Min(state.TemporaryHp,resolvedDamage), post=resolvedDamage-absorbed;
            long temp=state.TemporaryHp-absorbed, hp=Math.Max(0,state.Hp-post);
            // Signed difference is safe: both operands are nonnegative long quantities.
            long lost=state.Hp-hp;
            if (hp == 0 && post-state.Hp >= state.MaximumHp)
                return new DamageResolution(DeadState(state,temp,state.DeathFailures),post,absorbed,lost,true,null,null,0,0);

            var wounds=state.Wounds.ToList();
            long? dc=null, total=null;
            int injuryRolls=0, failuresAdded=0;
            bool trigger=(state.Hp > 0 && hp == 0) || post >= state.MaximumHp/2+state.MaximumHp%2 || maiming;
            if (trigger) {
                dc=Math.Max(10,post/2);
                // Supplied modifier excludes the Wound penalty; subtract pre-event count exactly once.
                total=(long)Die(woundNatural,20,"Wound-save d20")+constitutionSaveModifier-state.Wounds.Count;
                if (total.Value < dc.Value) {
                    if (wounds.Count == 3)
                        return new DamageResolution(DeadState(state,temp,state.DeathFailures),post,absorbed,lost,false,dc,total,0,0);
                    Injury injury=Injury.None;
                    if (dc.Value-total.Value >= 5) {
                        injury=(Injury)Die(injuryD6,6,"Injury d6"); injuryRolls=1;
                    }
                    wounds.Add(injury);
                }
            }
            bool stable=state.Stable, dead=false;
            long? deadline=state.StableUntilSeconds;
            int successes=state.DeathSuccesses, failures=state.DeathFailures;
            if (state.Hp == 0 && post > 0) {
                stable=false; deadline=null;
                if (!state.UsesDeathSaves) dead=true;
                else {
                    failuresAdded=critical ? 2 : 1;
                    failures=Math.Min(3,failures+failuresAdded);
                    dead=failures==3;
                }
            }
            if (state.Hp > 0 && hp == 0) {
                stable=false; deadline=null;
                if (knockout) {
                    int roll=Die(stableD4,4,"Stable recovery d4");
                    deadline=checked(nowSeconds+roll*3600L);
                    stable=true; successes=failures=0;
                } else if (!state.UsesDeathSaves) dead=true;
            }
            var result=new LifeState(state.MaximumHp,hp,temp,wounds,stable,dead,successes,failures,
                state.UsesDeathSaves,deadline,state.LastDeathTurn);
            return new DamageResolution(result,post,absorbed,lost,false,dc,total,injuryRolls,failuresAdded);
        }

        public static LifeState DeathSave(LifeState state, int natural, long regularTurnId, bool regular = true,
            int modifier = 0, int? stableD4 = null, long nowSeconds = 0, bool hpRecoveryProhibited = false)
        {
            RequireState(state); Die(natural,20,"death-save d20");
            if (nowSeconds < 0) throw new ArgumentOutOfRangeException(nameof(nowSeconds));
            if (!regular || regularTurnId <= 0 || regularTurnId <= state.LastDeathTurn)
                throw new ArgumentException("Death save requires a new regular-turn start.");
            if (state.Dead || state.Stable || state.Hp != 0 || !state.UsesDeathSaves)
                throw new ArgumentException("Creature is not dying with death saves.");
            if (natural == 20 && hpRecoveryProhibited) {
                // Reviewed Decay interface: no transient HP gain; clear counters and stabilize.
                long deadline=checked(nowSeconds+Die(stableD4,4,"Stable recovery d4")*3600L);
                return new LifeState(state.MaximumHp,0,state.TemporaryHp,state.Wounds,stable:true,
                    stableUntilSeconds:deadline,lastDeathTurn:regularTurnId);
            }
            if (natural == 20)
                return new LifeState(state.MaximumHp,1,state.TemporaryHp,state.Wounds,
                    usesDeathSaves:state.UsesDeathSaves,lastDeathTurn:regularTurnId);
            int successes=state.DeathSuccesses, failures=state.DeathFailures;
            if (natural == 1) failures+=2;
            else if ((long)natural+modifier >= 10) successes++;
            else failures++;
            if (failures >= 3)
                return new LifeState(state.MaximumHp,0,state.TemporaryHp,state.Wounds,dead:true,
                    deathSuccesses:successes,deathFailures:3,lastDeathTurn:regularTurnId);
            if (successes >= 3) {
                long deadline=checked(nowSeconds+Die(stableD4,4,"Stable recovery d4")*3600L);
                return new LifeState(state.MaximumHp,0,state.TemporaryHp,state.Wounds,stable:true,
                    stableUntilSeconds:deadline,lastDeathTurn:regularTurnId);
            }
            return new LifeState(state.MaximumHp,0,state.TemporaryHp,state.Wounds,deathSuccesses:successes,
                deathFailures:failures,lastDeathTurn:regularTurnId);
        }

        public static LifeState StableRecovery(LifeState state, long nowSeconds, bool hpRecoveryProhibited = false)
        {
            RequireState(state);
            if (nowSeconds < 0) throw new ArgumentOutOfRangeException(nameof(nowSeconds));
            return !hpRecoveryProhibited && state.Stable && state.StableUntilSeconds.HasValue && nowSeconds >= state.StableUntilSeconds.Value
                ? Heal(state,1) : state;
        }

        /// <summary>Caller supplies the separately resolved effective maximum. This is not an HP event.</summary>
        public static LifeState ChangeMaximum(LifeState state, long maximumHp)
        {
            RequireState(state);
            if (maximumHp < 1) throw new ArgumentOutOfRangeException(nameof(maximumHp));
            return new LifeState(maximumHp,Math.Min(state.Hp,maximumHp),state.TemporaryHp,state.Wounds,
                state.Stable,state.Dead,state.DeathSuccesses,state.DeathFailures,state.UsesDeathSaves,
                state.StableUntilSeconds,state.LastDeathTurn);
        }

        public static LifeState RemoveWounds(LifeState state, IReadOnlyList<int> indices)
        {
            RequireState(state);
            if (state.Dead) throw new ArgumentException("Ordinary treatment requires a living patient.");
            if (indices == null) throw new ArgumentNullException(nameof(indices));
            var selected=new HashSet<int>(indices);
            if (indices.Count == 0 || selected.Count != indices.Count || selected.Any(x=>x<0 || x>=state.Wounds.Count))
                throw new ArgumentException("Choose distinct existing Wound indices.",nameof(indices));
            return new LifeState(state.MaximumHp,state.Hp,state.TemporaryHp,state.Wounds.Where((x,i)=>!selected.Contains(i)),
                state.Stable,state.Dead,state.DeathSuccesses,state.DeathFailures,state.UsesDeathSaves,
                state.StableUntilSeconds,state.LastDeathTurn);
        }

        public static IReadOnlyList<Injury> ActiveInjuries(LifeState state)
        {
            RequireState(state);
            return Array.AsReadOnly(state.Wounds.Where(x=>x!=Injury.None).Distinct().OrderBy(x=>x).ToArray());
        }

        public static int HitDiceRecovered(int normalRecoveryMaximum, int wounds)
        {
            if (normalRecoveryMaximum < 0 || wounds < 0 || wounds > 3) throw new ArgumentOutOfRangeException(nameof(wounds));
            return Math.Max(0,normalRecoveryMaximum-wounds);
        }
    }
}
#endif
