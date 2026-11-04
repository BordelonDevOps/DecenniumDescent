#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Numerics;

namespace Decennium.Foundation.Laboratory
{
    [Flags] public enum OrdinaryStrikingParts { None=0, Fist=1, Elbow=2, Knee=4, Foot=8, Head=16 }
    /// <summary>Owner-adopted ordinary humanoid completion. Supplied usable body parts are facts,
    /// not anatomy/condition grants. Flat bludgeoning damage has no die to double on a critical.</summary>
    public static class PrototypeUnarmed
    {
        public static bool CanStrike(OrdinaryStrikingParts actuallyUsable)
        {
            if(((int)actuallyUsable&~31)!=0)throw new ArgumentException("Unsupported ordinary striking part.");
            return actuallyUsable!=OrdinaryStrikingParts.None;
        }
        public static long Damage(int strength,long applicableFlatModifiers=0)
            =>checked((long)BigInteger.Max(0,(BigInteger)1+PlaytestCharacters.AbilityModifier(strength)+applicableFlatModifiers));
    }
}
#endif
