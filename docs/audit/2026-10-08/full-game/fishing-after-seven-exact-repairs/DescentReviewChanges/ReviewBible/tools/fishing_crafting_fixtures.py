"""Explicit synthetic body/inventory records for FI-E10 regression checks."""
from copy import deepcopy
import fishing_reference as ref
from build_fishing_recipe_candidate import ROOT,read,model_id

CANDIDATE=read(ROOT/'data/director/fishing_recipe_candidate_internal.json')
CARDS={c['recipeId']:c for c in CANDIDATE['cards']}
MODELS=CANDIDATE['baseModels']


class CraftFixture:
    def __init__(self,recipe_id='recipe-163',band='Standard',option='yield',*,packaged=False,repair=False):
        self.records={};self.recipe=CARDS[recipe_id]['sourceRecipe'];self.model=MODELS[model_id(self.recipe)]
        self.cp=[3600,0,0];self.order_id='order-1';self.quality_id='quality-1'
        self.state_ids=[];self.repair=repair;self.band=band;self.option=option
        for i in range(1 if repair else 3*self.recipe['quantity']//2):
            body=f'body-{i}';creation=f'creation-{i}';inventory=f'inventory-{i}';reservation=f'reservation-{i}'
            roles={'exclusive-package'} if packaged else ref.PRIMARY_ROLES[self.model['family']]
            primary={role:[f'{body}-{role}'] for role in sorted(roles)}
            parts=[]
            for role,ids in primary.items():
                p={'physicalId':ids[0],'originalBodyId':body,'condition':'intact'}
                if role in ('carrier','wrapper'):
                    p.update({'materialCondition':'eligible','massLb':.1 if role=='carrier' else .01})
                if role=='exclusive-package':
                    p.update({'exclusivePackagedStock':True,'carrierCondition':'eligible','wrapperCondition':'eligible','carrierLb':.1,'wrapperLb':.01})
                if role=='functional-span':
                    p['recoveredOriginalSections']=[{'physicalId':ids[0]+'-whole','originalConstituentId':ids[0],
                        'startFeet':0,'endFeet':50,'condition':'intact'}]
                parts.append(p)
            self.add(creation,'body-creation',[0,0,0],physicalId=body,bodyModelId=self.model['id'],
                bodyProfile=self.model,primaryConstituents=primary,recipeId=recipe_id if repair else None,
                strongestDurabilityPercent=0,persistentFlaw=False,additionalIrreplaceableConstituentIds=[])
            state='available-for-repair' if repair else 'available-reserved'
            self.add(inventory,'body-inventory',self.cp,physicalId=body,constituents=parts,
                reservedForOrderId=None if repair else self.order_id,availability=state)
            self.add(reservation,'body-reservation',self.cp,physicalId=body,orderId=self.order_id,state='active')
            self.add(body,'crafting-body-state',self.cp,physicalId=body,bodyModelId=self.model['id'],
                creationEvidenceId=creation,inventoryEvidenceId=inventory,reservationEvidenceId=reservation,
                recipeId=recipe_id if repair else None,state=state,grade='Standard',priorMagicalAlteration=repair,
                complete=True,materialCondition='eligible',currentHP=self.model['ordinaryMaximumStructuralHP'],
                maximumHP=self.model['ordinaryMaximumStructuralHP'],durabilityPercent=0,flawed=False)
            self.state_ids.append(body)
        self.add(self.quality_id,'crafting-quality-resolution',self.cp,orderId=self.order_id,recipeId=recipe_id,band=band,option=option)
        self.add(self.order_id,'fishing-crafting-order',self.cp,recipeId=recipe_id,bodyModelId=self.model['id'],
            qualityResolutionEvidenceId=self.quality_id,orderedBodyStateIds=self.state_ids)

    def add(self,ident,kind,cp,**fields):
        self.records[ident]={'id':ident,'kind':kind,'checkpoint':list(cp),'authority':'synthetic FI-E10 fixture only',
            'citations':['GPT_FISHING_EXACT_OPERATIONAL_REVIEW.md FI-E10; local physical premises explicitly assumed'],
            'fixture':True,**deepcopy(fields)}

    def world(self):return ref.WorldEvidence(self.records,test_fixture=True)
    def reserves(self):return [deepcopy(self.records[k]) for k in self.state_ids]
    def outcome(self,band,option='yield'):
        self.band=band;self.option=option
        self.records[self.quality_id].update({'band':band,'option':option})
    def output(self):
        return ref.ordered_output(self.recipe,self.band,self.reserves(),self.option,
            world=self.world(),order_evidence_id=self.order_id,models=MODELS)
    def quote(self):return ref.qualified_repair_quote(self.world(),self.state_ids[0],CARDS,MODELS)
