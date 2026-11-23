using System;
using System.Globalization;
using System.Linq;
using System.Security.Cryptography;
using System.Text;

namespace Decennium.Foundation
{
    /// <summary>Opt-in host capability identity over the unchanged wire116 work records.
    /// Exact policy equality and causal verification remain required; this is not a history birthplace certificate.</summary>
    public static class ConnectedWorkControlProfile
    {
        public const string FingerprintPrefix = "TEST_ONLY.work-control-v1-";
        public const string Approval = "0918e51d-0813-51e4-abd8-111b4c240ec3";
        public const string ContractHash = "d65c7bcdf6c9ade960e70b527c82d71c367e4f883d180d91f0b299c8e13d8819";

        public static bool SelectedFingerprint(string value) => value != null
            && value.StartsWith(FingerprintPrefix, StringComparison.Ordinal)
            && CreatureActorRecord.Hex(value.Substring(FingerprintPrefix.Length), 64);

        public static string BindFingerprint(string ordinaryMagicFingerprint)
        {
            if (ordinaryMagicFingerprint == null
                || !ordinaryMagicFingerprint.StartsWith(OrdinaryMagicProfile.FingerprintPrefix, StringComparison.Ordinal)
                || !CreatureActorRecord.Hex(ordinaryMagicFingerprint.Substring(OrdinaryMagicProfile.FingerprintPrefix.Length), 64))
                throw new ArgumentException("Connected work control requires its exact ordinary-magic predecessor.");
            using (var hash = SHA256.Create()) return FingerprintPrefix + string.Concat(hash.ComputeHash(Encoding.UTF8.GetBytes(
                string.Join("|", ordinaryMagicFingerprint, Approval, ContractHash,
                    "water|mining|recipe4-research|recipe4-batch|host-controls-v1")))
                .Select(x => x.ToString("x2", CultureInfo.InvariantCulture)));
        }

        internal static bool MatchesOrdinaryMagic(string fingerprint, string predecessor)
        {
            string ordinary = OrdinaryMagicProfile.BindFingerprint(predecessor);
            return fingerprint == ordinary || fingerprint == BindFingerprint(ordinary);
        }
    }
}
