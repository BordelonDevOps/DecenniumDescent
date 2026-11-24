"""Share exact Strain recovery source branches and pre-write capacity guards."""
import re, runpy, subprocess
from pathlib import Path
h=runpy.run_path(str(Path(__file__).with_name('Extract-NativePreflight.py')))
root=h['ROOT']; lab='engine/com.decennium.foundation/Laboratory/Model/'

def baseline(path):
    return subprocess.check_output(['git','show',h['BASE']+':'+path],cwd=root).decode().replace('\r\n','\n')

def replace(path,old,new):
    p=root/path; raw=p.read_bytes(); eol='\r\n' if raw.count(b'\n')==raw.count(b'\r\n') else '\n'
    current=p.read_text(encoding='utf8'); assert current.count(old)==1,(path,old)
    p.write_bytes(current.replace(old,new,1).replace('\n',eol).encode())

configs=[
 ('SharedMoraleRest.cs','private string AssessSchema65RecoveryChoice(Snapshot s, Command c,\n            out ExpeditionStrainRecoveryOfferRecord offer, out ExpeditionStrainGainRecord gain)',
  '        private ExpeditionStrainGainRecord[] ExpeditionStrainRulesEligible(', 'Schema65RecoveryChoiceConstraintV1'),
 ('SharedStrainRecovery.cs','private string AssessStrainRecoveryChoice(Snapshot s, Command c, out ExpeditionStrainRecoveryOfferRecord offer,\n            out ExpeditionStrainGainRecord gain)',
  '        private string ResolveStrainRecoveryChoice(', 'StrainRecoveryChoiceConstraintV1')]
for file,signature,end,name in configs:
    path=lab+file; start='        '+signature; oldname=signature.split('string ')[1].split('(')[0]
    edits=[] if file=='SharedMoraleRest.cs' else [('return AssessSchema65RecoveryChoice(s, c, out offer, out gain);',
        'return Schema65RecoveryChoiceConstraintV1(s, c, out offer, out gain);')]
    h['extract'](path,start,end,name,start.replace('string '+oldname,'NativeCommandConstraintV1 '+name),
        start+'\n            => '+name+'(s,c,out offer,out gain)?.NativeCode;\n\n',edits)

for file,method in [('SharedMoraleRest.cs','Schema65'),('SharedStrainRecovery.cs','Generic')]:
    path=lab+file; source=baseline(path)
    fragment='''            if (s.ExpeditionStrainRemovals.Length >= ExpeditionProvisioningValidation.MaxStrainRemovals)
                return "ExpeditionStrainRecoveryHistoryCapacityReached";
'''
    line=source[:source.index('return "ExpeditionStrainRecoveryHistoryCapacityReached";')].count('\n')+1
    name=method+'StrainRemovalCapacityV1'
    helper='''        private static NativeCommandConstraintV1 '''+name+'''(Snapshot s)
            => s.ExpeditionStrainRemovals.Length >= ExpeditionProvisioningValidation.MaxStrainRemovals
                ? new NativeCommandConstraintV1("ExpeditionStrainRecoveryHistoryCapacityReached",
                    "'''+path+'", '+str(line)+''') : null;

'''
    replace(path,fragment,'            var capacityFailure='+name+'(s);\n            if(capacityFailure!=null)return capacityFailure.NativeCode;\n')
    anchor='        private string Resolve'+('Schema65RecoveryChoice' if method=='Schema65' else 'StrainRecoveryChoice')+'('
    replace(path,anchor,helper+anchor)

path=lab+'SharedStrainRecovery.cs'; source=baseline(path)
fragment='''                if (s.ExpeditionBeneficialRests.Length >= ExpeditionProvisioningValidation.MaxBeneficialRests)
                    return "ExpeditionBeneficialRestHistoryCapacityReached";
'''
start=source.index('        private string ResolveStrainRecoveryChoice(')
line=source[:source.index('return "ExpeditionBeneficialRestHistoryCapacityReached";',start)].count('\n')+1
current=(root/path).read_text(encoding='utf8')
a=current.index('        private string ResolveStrainRecoveryChoice(')
b=current.index('        private CommandQueryResult QueryStrainRecoveryChoice(',a)
body=current[a:b]; assert body.count(fragment)==1
replace(path,body,body.replace(fragment,'                var benefitCapacity=StrainBenefitCapacityV1(s);\n                if(benefitCapacity!=null)return benefitCapacity.NativeCode;\n'))
helper='''        private static NativeCommandConstraintV1 StrainBenefitCapacityV1(Snapshot s)
            => s.ExpeditionBeneficialRests.Length >= ExpeditionProvisioningValidation.MaxBeneficialRests
                ? new NativeCommandConstraintV1("ExpeditionBeneficialRestHistoryCapacityReached",
                    "'''+path+'", '+str(line)+''') : null;

        private NativeCommandConstraintV1 StrainRecoveryInitialConstraintV1(Snapshot s, Command c)
        {
            if(moraleRestProfile!=null && s.SchemaVersion>=Snapshot.MoraleRestSchema)
                return Schema65RecoveryChoiceConstraintV1(s,c,out _,out _) ?? Schema65StrainRemovalCapacityV1(s);
            var failure=StrainRecoveryChoiceConstraintV1(s,c,out var offer,out _)
                ?? GenericStrainRemovalCapacityV1(s);
            if(failure!=null)return failure;
            var benefit=s.ExpeditionBeneficialRests.SingleOrDefault(x=>x.RestIntervalId==offer.RestIntervalId
                &&x.ActorId==c.Actor&&x.RecoveryOfferId==offer.Id);
            return benefit==null?StrainBenefitCapacityV1(s):null;
        }

'''
anchor='        private static NativeCommandConstraintV1 GenericStrainRemovalCapacityV1('
replace(path,anchor,helper+anchor)
