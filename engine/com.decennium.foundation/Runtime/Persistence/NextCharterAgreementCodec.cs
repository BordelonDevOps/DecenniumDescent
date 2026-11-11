using System;
using System.IO;
using System.Linq;

namespace Decennium.Foundation
{
    internal static class NextCharterAgreementCodec
    {
        public static void Write(BinaryWriter writer, NextCharterAgreementRecord agreement)
        {
            writer.Write(agreement != null);
            if (agreement == null) return;

            void Text(string value) => SnapshotCodec.WriteText(writer, value);
            void Time(RuleTime value) { writer.Write(value.Numerator); writer.Write(value.Denominator); }

            Text(agreement.PlanId);
            var terms = agreement.Terms;
            foreach (string id in new[] { terms.OfferId, terms.CharterId, terms.CharterVersionId, terms.AssentAuthorityId,
                terms.RecordsAccessId, terms.ResourceUseAuthorityId, terms.ResourceOwnerId })
                Text(id);
            writer.Write((int)terms.SoloOffices);
            Time(terms.ValidFrom);
            Time(terms.ValidUntil);

            var permission = terms.AccessPermission;
            foreach (string id in new[] { permission.VersionId, permission.EvidenceId, permission.IssuerId,
                permission.IssuerAuthorityId, permission.BeneficiaryId, permission.MethodId, permission.RestrictionsId })
                Text(id);
            writer.Write(permission.StageX);
            writer.Write(permission.StageY);
            writer.Write(permission.ApproachX);
            writer.Write(permission.ApproachY);
            writer.Write((int)permission.Directions);
            Time(permission.ValidFrom);
            Time(permission.ValidUntil);
            writer.Write(permission.ChargeCopper);

            writer.Write(agreement.PlanReportRevision);
            writer.Write(agreement.PriorCloseRevision);
            Text(agreement.CommandId);
            writer.Write(agreement.AcceptedRevision);
            NextCharterPlanCodec.WriteObservation(writer, agreement.Observation);
            var withdrawal = agreement.Withdrawal;
            writer.Write(withdrawal != null);
            if (withdrawal != null) {
                Text(withdrawal.CommandId);
                writer.Write(withdrawal.Revision);
                Time(withdrawal.At);
            }
        }

        public static NextCharterAgreementRecord Read(BinaryReader reader, Snapshot state)
        {
            if (!SnapshotCodec.ReadBool(reader)) return null;
            string Text() => SnapshotCodec.ReadText(reader);
            RuleTime Time() => new RuleTime(reader.ReadInt64(), reader.ReadInt64());

            string planId = Text();
            var plan = state.NextCharterPlans.SingleOrDefault(x => x.Id == planId);
            if (plan?.Report == null) throw new ArgumentException("Prospective charter is missing its completed plan.");

            string offer = Text(), charter = Text(), charterVersion = Text(), mandate = Text(), records = Text(),
                useAuthority = Text(), owner = Text();
            var offices = (NextCharterOffice)reader.ReadInt32();
            var validFrom = Time();
            var validUntil = Time();

            string permissionId = Text(), evidence = Text(), issuer = Text(), issuerAuthority = Text(), beneficiary = Text(),
                method = Text(), restrictions = Text();
            var permission = new NextCharterAccessPermission(permissionId, evidence, issuer, issuerAuthority, beneficiary,
                reader.ReadInt32(), reader.ReadInt32(), reader.ReadInt32(), reader.ReadInt32(),
                (NextCharterPassageDirections)reader.ReadInt32(), method, Time(), Time(), reader.ReadInt64(), restrictions);
            var terms = new NextCharterAgreementTerms(offer, charter, charterVersion, mandate, records, useAuthority, owner,
                offices, plan.Terms, permission, validFrom, validUntil);

            long reportRevision = reader.ReadInt64(), priorClose = reader.ReadInt64();
            string commandId = Text();
            long acceptedRevision = reader.ReadInt64();
            var observation = NextCharterPlanCodec.ReadObservation(reader);
            var withdrawal = SnapshotCodec.ReadBool(reader) ? new NextCharterWithdrawal(Text(), reader.ReadInt64(), Time()) : null;
            return new NextCharterAgreementRecord(terms, planId, reportRevision, priorClose, commandId,
                acceptedRevision, observation, withdrawal);
        }
    }
}
