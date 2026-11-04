#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Linq;

namespace Decennium.Foundation.Laboratory
{
    // Every coordinate, wall, token and clock increment below is synthetic TEST_ONLY data.
    // No Decennium distance unit, cost, reward, combat cadence or elapsed-time conversion is implied.
    public sealed class TestOnlyPolicy : ICommandPolicy
    {
        public const string ActorId = "TEST_ONLY.actor";
        public const string CompanionId = "TEST_ONLY.companion";
        public const string ContainerId = "TEST_ONLY.container";
        public string ContentFingerprint => "TEST_ONLY.lab-v1";
        public bool TestOnly => true;
        public static Authority Host() => new Authority("TEST_ONLY.host", new[] { ActorId, CompanionId }, true);
        public Snapshot Initial() => new Snapshot {
            ContentFingerprint = ContentFingerprint, TestOnly = true, RandomState = 1,
            Actors = new[] { new ActorState { Id = ActorId, X = 1, Y = 1 }, new ActorState { Id = CompanionId, X = 3, Y = 3 } },
            Objects = new[] { new ObjectState { Id = ContainerId, X = 1, Y = 2 } }, Receipts = Array.Empty<CommandReceipt>()
        };
        public static bool Walkable(int x, int y) => x >= 0 && x < 5 && y >= 0 && y < 5 && !(x == 2 && y == 1);
        public string ValidateState(Snapshot state)
        {
            if (state.SchemaVersion != Snapshot.Schema) return "WrongFixtureSchema";
            return ValidateWorld(state);
        }
        internal static string ValidateWorld(Snapshot state)
        {
            bool third=state.SchemaVersion==Snapshot.TacticalMovementSchema&&state.Actors.Any(a=>a.Id==AdditionalTacticalActor.Id);
            if (state.Actors.Length != (third?3:2) || !state.Actors.Any(a => a.Id == ActorId) || !state.Actors.Any(a => a.Id == CompanionId)
                || state.Objects.Length != 1 || state.Objects[0].Id != ContainerId || state.Objects[0].X != 1 || state.Objects[0].Y != 2)
                return "UnknownFixtureIdentity";
            if (state.Actors.Any(a => !Walkable(a.X, a.Y) || a.Tokens > 1)
                || state.Actors.Select(a => a.X + "," + a.Y).Distinct().Count() != state.Actors.Length) return "InvalidFixturePosition";
            if (state.Actors.Sum(a => a.Tokens) != (state.Objects[0].Opened ? 1 : 0)) return "InvalidFixtureTokenBalance";
            return null;
        }
        public string Resolve(Snapshot state, Command command)
        {
            ActorState actor = state.Actors.Single(a => a.Id == command.Actor);
            switch (command.Kind)
            {
                case CommandKind.Move:
                    if (command.Target != "" || Math.Abs((long)command.X) + Math.Abs((long)command.Y) != 1) return "InvalidStep";
                    int x = checked(actor.X + command.X), y = checked(actor.Y + command.Y);
                    if (!Walkable(x, y)) return "Blocked";
                    if (state.Actors.Any(a => a.Id != actor.Id && a.X == x && a.Y == y)) return "Occupied";
                    actor.X = x; actor.Y = y; return null;
                case CommandKind.Interact:
                    if (command.X != 0 || command.Y != 0) return "InvalidInteraction";
                    ObjectState obj = state.Objects.FirstOrDefault(o => o.Id == command.Target);
                    if (obj == null) return "UnknownObject";
                    if (Math.Abs(actor.X - obj.X) + Math.Abs(actor.Y - obj.Y) > 1) return "OutOfReach";
                    if (obj.Opened) return "AlreadyOpened";
                    actor.Tokens = checked(actor.Tokens + 1); obj.Opened = true; return null;
                case CommandKind.AdvanceClock:
                    if (command.Target != "" || command.Y != 0 || command.X < 1 || command.X > 10) return "InvalidClockAdvance";
                    state.Clock = checked(state.Clock + command.X); return null;
                default: return "UnsupportedCommand";
            }
        }
    }
}
#endif
