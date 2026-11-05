using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Globalization;
using System.Linq;

namespace Decennium.Foundation.Laboratory
{
    public enum ClassAdvancementScheduleKind { Structured, NarrativeException }

    /// <summary>Immutable source row. A narrative exception never becomes an empty schedule by implication.</summary>
    public sealed class ClassAdvancementScheduleRow
    {
        private readonly string[] bands;
        public string ClassName { get; }
        public int ClassLevel { get; }
        public ClassAdvancementScheduleKind Kind { get; }
        public int? RequiredSelections { get; }
        public ReadOnlyCollection<string> Bands { get; }
        public int? MinimumActiveSelections { get; }
        public bool? HasAsiOrFeatOpportunity { get; }
        public string SourcePath { get; }
        public string SourceLocator { get; }
        internal ClassAdvancementScheduleRow(string className,int classLevel,ClassAdvancementScheduleKind kind,int? requiredSelections,
            string[] bands,int? minimumActiveSelections,bool? hasAsiOrFeatOpportunity,string sourcePath,string sourceLocator)
        {
            var values=bands??Array.Empty<string>();
            bool locatorOk=sourceLocator!=null&&(sourceLocator.StartsWith("/schedule/",StringComparison.Ordinal)
                ||sourceLocator.StartsWith("/exceptionSchedule/",StringComparison.Ordinal));
            if(string.IsNullOrEmpty(className)||className.Length>96||classLevel<1||classLevel>20
                ||!Enum.IsDefined(typeof(ClassAdvancementScheduleKind),kind)||string.IsNullOrEmpty(sourcePath)||!locatorOk
                ||values.Distinct(StringComparer.Ordinal).Count()!=values.Length
                ||kind==ClassAdvancementScheduleKind.Structured&&(requiredSelections<0||requiredSelections>16||minimumActiveSelections<0
                    ||minimumActiveSelections>requiredSelections||hasAsiOrFeatOpportunity==null
                    ||values.Any(x=>x!="Base"&&x!="Arch"&&x!="Hero")||requiredSelections==0&&values.Length!=0||requiredSelections>0&&values.Length==0)
                ||kind==ClassAdvancementScheduleKind.NarrativeException&&(requiredSelections.HasValue||values.Length!=0||minimumActiveSelections.HasValue||hasAsiOrFeatOpportunity.HasValue))
                throw new ArgumentException("Invalid class advancement schedule row.");
            ClassName=className;ClassLevel=classLevel;Kind=kind;RequiredSelections=requiredSelections;
            this.bands=values.ToArray();Bands=Array.AsReadOnly(this.bands);MinimumActiveSelections=minimumActiveSelections;
            HasAsiOrFeatOpportunity=hasAsiOrFeatOpportunity;SourcePath=sourcePath;SourceLocator=sourceLocator;
        }
    }

    /// <summary>Exact finite projection of pinned authored class acquisition rows. It supplies schedule facts only;
    /// card prerequisites, automatic engines, class resources, ASI/feat procedures and runtime handlers remain separately bound.</summary>
    public static class ClassAdvancementScheduleCatalog
    {
        public const string SourceRevision="46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4";
        private const string SourceFilesData=
            "Bard|DescentReviewChanges/ReviewBible/data/public/Decennium_Descent_Bard_Playtest_v0_1.json|b514ef61a468d5d9b19031811f98860f1a61324b4626df601d2748dcb46ce6a6|bad7a48f9e11da6d3069d94955183f59d1b1ceb1|complete-card-draft-not-balance-approved;" +
            "Cleric|DescentReviewChanges/ReviewBible/data/public/class_playtests/cleric.json|25387b0dcfae0d53d689486d4b05d8ef5b24bed1b70f0baab970a82dbd370f89|193ca1eaecd1c9fa1f26993dfe872f7da2a17b97|provisional-card-draft-not-balance-approved;" +
            "Crimson Agent|DescentReviewChanges/ReviewBible/data/public/class_playtests/crimson-agent.json|bfcd0ff392035e48bdef27da630b911b96ce85ba036de5de622cdc2427a47a33|ffc81b6d70155cd38b9ddc0a26674317910ebaf5|provisional-card-draft-not-balance-approved;" +
            "Dragoon|DescentReviewChanges/ReviewBible/data/public/class_playtests/dragoon.json|b55a59ae743bc1b8ed0d5832eb40453f438bc9c9f4a69aef87f3e19048e0fb0e|185a4f28930cf0757846aa5200b79c10da0a75c5|provisional-card-draft-not-balance-approved;" +
            "Druid|DescentReviewChanges/ReviewBible/data/public/class_playtests/druid.json|581bd030286dc91e17792e9724e942b99d7e7d97ce6f6a3dfacc4f37f5113b8f|e6778fbc21a547e235fcb1534eef27e553d1354b|provisional-card-draft-not-balance-approved;" +
            "Mage|DescentReviewChanges/ReviewBible/data/public/class_playtests/mage.json|c64782e192e2e63e5abed5728f9213c9d4cf956bce1a75da7a156dbfd1141e0b|fa74b85e206a514991a7637870004a7ddd91925b|provisional-card-draft-not-balance-approved;" +
            "Mirrorsage|DescentReviewChanges/ReviewBible/data/public/class_playtests/mirrorsage.json|9179729dd39e0a81f4f6d78b9fbb0c7fb296fb5d418aaa238d7ff6aa02b2bd3a|e08bed18fbca8e67e424cf3c90214488fb760da2|provisional-card-draft-not-balance-approved;" +
            "Monk|DescentReviewChanges/ReviewBible/data/public/class_playtests/monk.json|18a8bac9168cb4c87c641b4f2e792d31ed5ae2ae56240b3fbeced9f6ada74fc9|55b02721365f94da339654a5075928e3bcca033f|provisional-card-draft-not-balance-approved;" +
            "Oracle|DescentReviewChanges/ReviewBible/data/public/class_playtests/oracle.json|fda69f674d24eab725957d07e04d79a92a48d9d2e28615e47ffd98046b80e327|2b4c1b5dedfe26be01161e7f64f51ed189253228|provisional-card-draft-not-balance-approved;" +
            "Paladin|DescentReviewChanges/ReviewBible/data/public/class_playtests/paladin.json|f028a253a1a08dd17e42a2abbcd3d7f7a484ea9d8255c934339bdf1739ae8e09|eed5f0ad8dbba80242b5f730c99d9a3c0f96162f|provisional-card-draft-not-balance-approved;" +
            "Ranger|DescentReviewChanges/ReviewBible/data/public/class_playtests/ranger.json|ae6b884b8ca2d1c89034d2c16a48e6e4b8061d0a774158cb7f5159557cbea326|550a52031e797d9a5f369050bfef3e44a994b1c5|provisional-card-draft-not-balance-approved;" +
            "Shaman|DescentReviewChanges/ReviewBible/data/public/class_playtests/shaman.json|c88fcad8c14734cc852a95aee7b3686fd64ea2a8cfb9d014f4297b7efec94a62|3746e45c76060c7b5a7bfcf27ed84c0ad6dc02c9|provisional-card-draft-not-balance-approved;" +
            "Soldier|DescentReviewChanges/ReviewBible/data/public/class_playtests/soldier.json|ab9cd3bd64355166dceb5a09e1ddab98443a957bb4bcdce813f1ad294ec048f0|c414a1d9ba2ce37cde89d0ef73265821bb74ac2d|provisional-card-draft-not-balance-approved;" +
            "Thief|DescentReviewChanges/ReviewBible/data/public/class_playtests/thief.json|9c2896fbf19bd3f1138707db2545b19156341c0a6e9be6a15192b19582068400|3b1db8b2586124146e78dd6c1c88f0b5ba44a460|provisional-card-draft-not-balance-approved;" +
            "Tinker|DescentReviewChanges/ReviewBible/data/public/class_playtests/tinker.json|f087cc9250f1864e60209fb13bff86800d45b7238dc09e8eac2dbf2272b09c1d|3a62b881428dae508e9c96f41f7968220d332325|provisional-card-draft-not-balance-approved;" +
            "Warrior|DescentReviewChanges/ReviewBible/data/public/class_playtests/warrior.json|b695808e3ad03411f0c482af40da964c8d2bac3235eb7c5f8953d27ed73a11b7|7376db19c5e3c499a994cb06eae06cf25514e922|provisional-card-draft-not-balance-approved;" +
            "Wizard|DescentReviewChanges/ReviewBible/data/public/class_playtests/wizard.json|8ab2f4f43bcbced418fb266e5bd3216cff491b0c442c16f93438bd3556672c8b|cba2bdbbe964e9597011ed59f0c934bd09350a93|provisional-card-draft-not-balance-approved;";
        private static readonly string[] EncodedRows=new string[] {
            "S|Bard|1|4|Base|2|0|/schedule/0",
            "S|Bard|2|2|Base|0|0|/schedule/1",
            "S|Bard|3|2|Arch|1|0|/schedule/2",
            "S|Bard|4|1|Base,Arch|0|1|/schedule/3",
            "S|Bard|5|1|Arch|0|0|/schedule/4",
            "S|Bard|6|1|Base,Arch|0|0|/schedule/5",
            "S|Bard|7|1|Arch|0|0|/schedule/6",
            "S|Bard|8|1|Base,Arch|0|1|/schedule/7",
            "S|Bard|9|1|Arch|0|0|/schedule/8",
            "S|Bard|10|2|Hero|1|0|/schedule/9",
            "S|Bard|11|1|Base,Arch|0|0|/schedule/10",
            "S|Bard|12|1|Hero|0|1|/schedule/11",
            "S|Bard|13|1|Base,Arch|0|0|/schedule/12",
            "S|Bard|14|1|Hero|0|0|/schedule/13",
            "S|Bard|15|1|Base,Arch|0|0|/schedule/14",
            "S|Bard|16|1|Hero|0|1|/schedule/15",
            "S|Bard|17|1|Base,Arch|0|0|/schedule/16",
            "S|Bard|18|1|Hero|0|0|/schedule/17",
            "S|Bard|19|1|Base,Arch|0|1|/schedule/18",
            "S|Bard|20|0|-|0|0|/schedule/19",
            "S|Cleric|1|4|Base|2|0|/schedule/0",
            "S|Cleric|2|2|Base|0|0|/schedule/1",
            "S|Cleric|3|2|Arch|1|0|/schedule/2",
            "S|Cleric|4|1|Base,Arch|0|1|/schedule/3",
            "S|Cleric|5|1|Base,Arch|0|0|/schedule/4",
            "S|Cleric|6|1|Base,Arch|0|0|/schedule/5",
            "S|Cleric|7|1|Base,Arch|0|0|/schedule/6",
            "S|Cleric|8|1|Base,Arch|0|1|/schedule/7",
            "S|Cleric|9|1|Arch|0|0|/schedule/8",
            "S|Cleric|10|2|Hero|1|0|/schedule/9",
            "S|Cleric|11|1|Base,Arch|0|0|/schedule/10",
            "S|Cleric|12|1|Hero|0|1|/schedule/11",
            "S|Cleric|13|1|Base,Arch|0|0|/schedule/12",
            "S|Cleric|14|1|Hero|0|0|/schedule/13",
            "S|Cleric|15|1|Base,Arch|0|0|/schedule/14",
            "S|Cleric|16|1|Hero|0|1|/schedule/15",
            "S|Cleric|17|1|Base,Arch|0|0|/schedule/16",
            "S|Cleric|18|1|Hero|0|0|/schedule/17",
            "S|Cleric|19|1|Base,Arch|0|1|/schedule/18",
            "S|Cleric|20|0|-|0|0|/schedule/19",
            "S|Crimson Agent|1|4|Base|2|0|/schedule/0",
            "S|Crimson Agent|2|2|Base|0|0|/schedule/1",
            "S|Crimson Agent|3|2|Arch|1|0|/schedule/2",
            "S|Crimson Agent|4|1|Base,Arch|0|1|/schedule/3",
            "S|Crimson Agent|5|1|Arch|0|0|/schedule/4",
            "S|Crimson Agent|6|1|Base,Arch|0|0|/schedule/5",
            "S|Crimson Agent|7|1|Arch|0|0|/schedule/6",
            "S|Crimson Agent|8|1|Base,Arch|0|1|/schedule/7",
            "S|Crimson Agent|9|1|Arch|0|0|/schedule/8",
            "S|Crimson Agent|10|2|Hero|1|0|/schedule/9",
            "S|Crimson Agent|11|1|Base,Arch|0|0|/schedule/10",
            "S|Crimson Agent|12|1|Hero|0|1|/schedule/11",
            "S|Crimson Agent|13|1|Base,Arch|0|0|/schedule/12",
            "S|Crimson Agent|14|1|Hero|0|0|/schedule/13",
            "S|Crimson Agent|15|1|Base,Arch|0|0|/schedule/14",
            "S|Crimson Agent|16|1|Hero|0|1|/schedule/15",
            "S|Crimson Agent|17|1|Base,Arch|0|0|/schedule/16",
            "S|Crimson Agent|18|1|Hero|0|0|/schedule/17",
            "S|Crimson Agent|19|1|Base,Arch|0|1|/schedule/18",
            "S|Crimson Agent|20|0|-|0|0|/schedule/19",
            "S|Dragoon|1|4|Base|2|0|/schedule/0",
            "S|Dragoon|2|2|Base|0|0|/schedule/1",
            "S|Dragoon|3|2|Arch|1|0|/schedule/2",
            "S|Dragoon|4|1|Base,Arch|0|1|/schedule/3",
            "S|Dragoon|5|1|Arch|0|0|/schedule/4",
            "S|Dragoon|6|1|Base,Arch|0|0|/schedule/5",
            "S|Dragoon|7|1|Arch|0|0|/schedule/6",
            "S|Dragoon|8|1|Base,Arch|0|1|/schedule/7",
            "S|Dragoon|9|1|Arch|0|0|/schedule/8",
            "S|Dragoon|10|2|Hero|1|0|/schedule/9",
            "S|Dragoon|11|1|Base,Arch|0|0|/schedule/10",
            "S|Dragoon|12|1|Hero|0|1|/schedule/11",
            "S|Dragoon|13|1|Base,Arch|0|0|/schedule/12",
            "S|Dragoon|14|1|Hero|0|0|/schedule/13",
            "S|Dragoon|15|1|Base,Arch|0|0|/schedule/14",
            "S|Dragoon|16|1|Hero|0|1|/schedule/15",
            "S|Dragoon|17|1|Base,Arch|0|0|/schedule/16",
            "S|Dragoon|18|1|Hero|0|0|/schedule/17",
            "S|Dragoon|19|1|Base,Arch|0|1|/schedule/18",
            "S|Dragoon|20|0|-|0|0|/schedule/19",
            "E|Druid|1|/exceptionSchedule/1",
            "E|Druid|2|/exceptionSchedule/2",
            "E|Druid|3|/exceptionSchedule/3",
            "E|Druid|4|/exceptionSchedule/4",
            "E|Druid|5|/exceptionSchedule/5",
            "E|Druid|6|/exceptionSchedule/6",
            "E|Druid|7|/exceptionSchedule/7",
            "E|Druid|8|/exceptionSchedule/8",
            "E|Druid|9|/exceptionSchedule/9",
            "E|Druid|10|/exceptionSchedule/10",
            "E|Druid|11|/exceptionSchedule/11",
            "E|Druid|12|/exceptionSchedule/12",
            "E|Druid|13|/exceptionSchedule/13",
            "E|Druid|14|/exceptionSchedule/14",
            "E|Druid|15|/exceptionSchedule/15",
            "E|Druid|16|/exceptionSchedule/16",
            "E|Druid|17|/exceptionSchedule/17",
            "E|Druid|18|/exceptionSchedule/18",
            "E|Druid|19|/exceptionSchedule/19",
            "E|Druid|20|/exceptionSchedule/20",
            "S|Mage|1|4|Base|2|0|/schedule/0",
            "S|Mage|2|2|Base|0|0|/schedule/1",
            "S|Mage|3|2|Arch|1|0|/schedule/2",
            "S|Mage|4|1|Base,Arch|0|1|/schedule/3",
            "S|Mage|5|1|Base,Arch|0|0|/schedule/4",
            "S|Mage|6|1|Base,Arch|0|0|/schedule/5",
            "S|Mage|7|1|Base,Arch|0|0|/schedule/6",
            "S|Mage|8|1|Base,Arch|0|1|/schedule/7",
            "S|Mage|9|1|Base,Arch|0|0|/schedule/8",
            "S|Mage|10|2|Hero|1|0|/schedule/9",
            "S|Mage|11|1|Base,Arch|0|0|/schedule/10",
            "S|Mage|12|1|Hero|0|1|/schedule/11",
            "S|Mage|13|1|Base,Arch|0|0|/schedule/12",
            "S|Mage|14|1|Hero|0|0|/schedule/13",
            "S|Mage|15|1|Base,Arch|0|0|/schedule/14",
            "S|Mage|16|1|Hero|0|1|/schedule/15",
            "S|Mage|17|1|Base,Arch|0|0|/schedule/16",
            "S|Mage|18|1|Hero|0|0|/schedule/17",
            "S|Mage|19|1|Base,Arch|0|1|/schedule/18",
            "S|Mage|20|1|Hero|0|0|/schedule/19",
            "S|Mirrorsage|1|4|Base|2|0|/schedule/0",
            "S|Mirrorsage|2|2|Base|0|0|/schedule/1",
            "S|Mirrorsage|3|2|Arch|1|0|/schedule/2",
            "S|Mirrorsage|4|1|Base,Arch|0|1|/schedule/3",
            "S|Mirrorsage|5|1|Arch|0|0|/schedule/4",
            "S|Mirrorsage|6|1|Base,Arch|0|0|/schedule/5",
            "S|Mirrorsage|7|1|Arch|0|0|/schedule/6",
            "S|Mirrorsage|8|1|Base,Arch|0|1|/schedule/7",
            "S|Mirrorsage|9|1|Arch|0|0|/schedule/8",
            "S|Mirrorsage|10|2|Hero|1|0|/schedule/9",
            "S|Mirrorsage|11|1|Base,Arch|0|0|/schedule/10",
            "S|Mirrorsage|12|1|Hero|0|1|/schedule/11",
            "S|Mirrorsage|13|1|Base,Arch|0|0|/schedule/12",
            "S|Mirrorsage|14|1|Hero|0|0|/schedule/13",
            "S|Mirrorsage|15|1|Base,Arch|0|0|/schedule/14",
            "S|Mirrorsage|16|1|Hero|0|1|/schedule/15",
            "S|Mirrorsage|17|1|Base,Arch|0|0|/schedule/16",
            "S|Mirrorsage|18|1|Hero|0|0|/schedule/17",
            "S|Mirrorsage|19|1|Base,Arch|0|1|/schedule/18",
            "S|Mirrorsage|20|0|-|0|0|/schedule/19",
            "S|Monk|1|4|Base|2|0|/schedule/0",
            "S|Monk|2|2|Base|0|0|/schedule/1",
            "S|Monk|3|2|Arch|1|0|/schedule/2",
            "S|Monk|4|1|Base,Arch|0|1|/schedule/3",
            "S|Monk|5|1|Arch|0|0|/schedule/4",
            "S|Monk|6|1|Base,Arch|0|0|/schedule/5",
            "S|Monk|7|1|Arch|0|0|/schedule/6",
            "S|Monk|8|1|Base,Arch|0|1|/schedule/7",
            "S|Monk|9|1|Arch|0|0|/schedule/8",
            "S|Monk|10|2|Hero|1|0|/schedule/9",
            "S|Monk|11|1|Base,Arch|0|0|/schedule/10",
            "S|Monk|12|1|Hero|0|1|/schedule/11",
            "S|Monk|13|1|Base,Arch|0|0|/schedule/12",
            "S|Monk|14|1|Hero|0|0|/schedule/13",
            "S|Monk|15|1|Base,Arch|0|0|/schedule/14",
            "S|Monk|16|1|Hero|0|1|/schedule/15",
            "S|Monk|17|1|Base,Arch|0|0|/schedule/16",
            "S|Monk|18|1|Hero|0|0|/schedule/17",
            "S|Monk|19|1|Base,Arch|0|1|/schedule/18",
            "S|Monk|20|0|-|0|0|/schedule/19",
            "E|Oracle|1|/exceptionSchedule/1",
            "E|Oracle|2|/exceptionSchedule/2",
            "E|Oracle|3|/exceptionSchedule/3",
            "E|Oracle|4|/exceptionSchedule/4",
            "E|Oracle|5|/exceptionSchedule/5",
            "E|Oracle|6|/exceptionSchedule/6",
            "E|Oracle|7|/exceptionSchedule/7",
            "E|Oracle|8|/exceptionSchedule/8",
            "E|Oracle|9|/exceptionSchedule/9",
            "E|Oracle|10|/exceptionSchedule/10",
            "E|Oracle|11|/exceptionSchedule/11",
            "E|Oracle|12|/exceptionSchedule/12",
            "E|Oracle|13|/exceptionSchedule/13",
            "E|Oracle|14|/exceptionSchedule/14",
            "E|Oracle|15|/exceptionSchedule/15",
            "E|Oracle|16|/exceptionSchedule/16",
            "E|Oracle|17|/exceptionSchedule/17",
            "E|Oracle|18|/exceptionSchedule/18",
            "E|Oracle|19|/exceptionSchedule/19",
            "E|Oracle|20|/exceptionSchedule/20",
            "E|Paladin|1|/exceptionSchedule/1",
            "E|Paladin|2|/exceptionSchedule/2",
            "E|Paladin|3|/exceptionSchedule/3",
            "E|Paladin|4|/exceptionSchedule/4",
            "E|Paladin|5|/exceptionSchedule/5",
            "E|Paladin|6|/exceptionSchedule/6",
            "E|Paladin|7|/exceptionSchedule/7",
            "E|Paladin|8|/exceptionSchedule/8",
            "E|Paladin|9|/exceptionSchedule/9",
            "E|Paladin|10|/exceptionSchedule/10",
            "E|Paladin|11|/exceptionSchedule/11",
            "E|Paladin|12|/exceptionSchedule/12",
            "E|Paladin|13|/exceptionSchedule/13",
            "E|Paladin|14|/exceptionSchedule/14",
            "E|Paladin|15|/exceptionSchedule/15",
            "E|Paladin|16|/exceptionSchedule/16",
            "E|Paladin|17|/exceptionSchedule/17",
            "E|Paladin|18|/exceptionSchedule/18",
            "E|Paladin|19|/exceptionSchedule/19",
            "E|Paladin|20|/exceptionSchedule/20",
            "S|Ranger|1|4|Base|2|0|/schedule/0",
            "S|Ranger|2|2|Base|0|0|/schedule/1",
            "S|Ranger|3|2|Arch|1|0|/schedule/2",
            "S|Ranger|4|1|Base,Arch|0|1|/schedule/3",
            "S|Ranger|5|1|Arch|0|0|/schedule/4",
            "S|Ranger|6|1|Base,Arch|0|0|/schedule/5",
            "S|Ranger|7|1|Arch|0|0|/schedule/6",
            "S|Ranger|8|1|Base,Arch|0|1|/schedule/7",
            "S|Ranger|9|1|Arch|0|0|/schedule/8",
            "S|Ranger|10|2|Hero|1|0|/schedule/9",
            "S|Ranger|11|1|Base,Arch|0|0|/schedule/10",
            "S|Ranger|12|1|Hero|0|1|/schedule/11",
            "S|Ranger|13|1|Base,Arch|0|0|/schedule/12",
            "S|Ranger|14|1|Hero|0|0|/schedule/13",
            "S|Ranger|15|1|Base,Arch|0|0|/schedule/14",
            "S|Ranger|16|1|Hero|0|1|/schedule/15",
            "S|Ranger|17|1|Base,Arch|0|0|/schedule/16",
            "S|Ranger|18|1|Hero|0|0|/schedule/17",
            "S|Ranger|19|1|Base,Arch|0|1|/schedule/18",
            "S|Ranger|20|0|-|0|0|/schedule/19",
            "S|Shaman|1|4|Base|2|0|/schedule/0",
            "S|Shaman|2|2|Base|0|0|/schedule/1",
            "S|Shaman|3|2|Arch|1|0|/schedule/2",
            "S|Shaman|4|1|Base,Arch|0|1|/schedule/3",
            "S|Shaman|5|1|Arch|0|0|/schedule/4",
            "S|Shaman|6|1|Base,Arch|0|0|/schedule/5",
            "S|Shaman|7|1|Arch|0|0|/schedule/6",
            "S|Shaman|8|1|Base,Arch|0|1|/schedule/7",
            "S|Shaman|9|1|Arch|0|0|/schedule/8",
            "S|Shaman|10|2|Hero|1|0|/schedule/9",
            "S|Shaman|11|1|Base,Arch|0|0|/schedule/10",
            "S|Shaman|12|1|Hero|0|1|/schedule/11",
            "S|Shaman|13|1|Base,Arch|0|0|/schedule/12",
            "S|Shaman|14|1|Hero|0|0|/schedule/13",
            "S|Shaman|15|1|Base,Arch|0|0|/schedule/14",
            "S|Shaman|16|1|Hero|0|1|/schedule/15",
            "S|Shaman|17|1|Base,Arch|0|0|/schedule/16",
            "S|Shaman|18|1|Hero|0|0|/schedule/17",
            "S|Shaman|19|1|Base,Arch|0|1|/schedule/18",
            "S|Shaman|20|0|-|0|0|/schedule/19",
            "S|Soldier|1|4|Base|2|0|/schedule/0",
            "S|Soldier|2|2|Base|0|0|/schedule/1",
            "S|Soldier|3|2|Arch|1|0|/schedule/2",
            "S|Soldier|4|1|Base,Arch|0|1|/schedule/3",
            "S|Soldier|5|1|Arch|0|0|/schedule/4",
            "S|Soldier|6|1|Base,Arch|0|0|/schedule/5",
            "S|Soldier|7|1|Arch|0|0|/schedule/6",
            "S|Soldier|8|1|Base,Arch|0|1|/schedule/7",
            "S|Soldier|9|1|Arch|0|0|/schedule/8",
            "S|Soldier|10|2|Hero|1|0|/schedule/9",
            "S|Soldier|11|1|Base,Arch|0|0|/schedule/10",
            "S|Soldier|12|1|Hero|0|1|/schedule/11",
            "S|Soldier|13|1|Base,Arch|0|0|/schedule/12",
            "S|Soldier|14|1|Hero|0|0|/schedule/13",
            "S|Soldier|15|1|Base,Arch|0|0|/schedule/14",
            "S|Soldier|16|1|Hero|0|1|/schedule/15",
            "S|Soldier|17|1|Base,Arch|0|0|/schedule/16",
            "S|Soldier|18|1|Hero|0|0|/schedule/17",
            "S|Soldier|19|1|Base,Arch|0|1|/schedule/18",
            "S|Soldier|20|0|-|0|0|/schedule/19",
            "S|Thief|1|4|Base|2|0|/schedule/0",
            "S|Thief|2|2|Base|0|0|/schedule/1",
            "S|Thief|3|2|Arch|1|0|/schedule/2",
            "S|Thief|4|1|Base,Arch|0|1|/schedule/3",
            "S|Thief|5|1|Arch|0|0|/schedule/4",
            "S|Thief|6|1|Base,Arch|0|0|/schedule/5",
            "S|Thief|7|1|Arch|0|0|/schedule/6",
            "S|Thief|8|1|Base,Arch|0|1|/schedule/7",
            "S|Thief|9|1|Arch|0|0|/schedule/8",
            "S|Thief|10|2|Hero|1|0|/schedule/9",
            "S|Thief|11|1|Base,Arch|0|0|/schedule/10",
            "S|Thief|12|1|Hero|0|1|/schedule/11",
            "S|Thief|13|1|Base,Arch|0|0|/schedule/12",
            "S|Thief|14|1|Hero|0|0|/schedule/13",
            "S|Thief|15|1|Base,Arch|0|0|/schedule/14",
            "S|Thief|16|1|Hero|0|1|/schedule/15",
            "S|Thief|17|1|Base,Arch|0|0|/schedule/16",
            "S|Thief|18|1|Hero|0|0|/schedule/17",
            "S|Thief|19|1|Base,Arch|0|1|/schedule/18",
            "S|Thief|20|0|-|0|0|/schedule/19",
            "S|Tinker|1|4|Base|2|0|/schedule/0",
            "S|Tinker|2|2|Base|0|0|/schedule/1",
            "S|Tinker|3|2|Arch|1|0|/schedule/2",
            "S|Tinker|4|1|Base,Arch|0|1|/schedule/3",
            "S|Tinker|5|1|Arch|0|0|/schedule/4",
            "S|Tinker|6|1|Base,Arch|0|0|/schedule/5",
            "S|Tinker|7|1|Arch|0|0|/schedule/6",
            "S|Tinker|8|1|Base,Arch|0|1|/schedule/7",
            "S|Tinker|9|1|Arch|0|0|/schedule/8",
            "S|Tinker|10|2|Hero|1|0|/schedule/9",
            "S|Tinker|11|1|Base,Arch|0|0|/schedule/10",
            "S|Tinker|12|1|Hero|0|1|/schedule/11",
            "S|Tinker|13|1|Base,Arch|0|0|/schedule/12",
            "S|Tinker|14|1|Hero|0|0|/schedule/13",
            "S|Tinker|15|1|Base,Arch|0|0|/schedule/14",
            "S|Tinker|16|1|Hero|0|1|/schedule/15",
            "S|Tinker|17|1|Base,Arch|0|0|/schedule/16",
            "S|Tinker|18|1|Hero|0|0|/schedule/17",
            "S|Tinker|19|1|Base,Arch|0|1|/schedule/18",
            "S|Tinker|20|0|-|0|0|/schedule/19",
            "S|Warrior|1|4|Base|2|0|/schedule/0",
            "S|Warrior|2|2|Base|0|0|/schedule/1",
            "S|Warrior|3|2|Arch|1|0|/schedule/2",
            "S|Warrior|4|1|Base,Arch|0|1|/schedule/3",
            "S|Warrior|5|1|Base,Arch|0|0|/schedule/4",
            "S|Warrior|6|1|Base,Arch|0|0|/schedule/5",
            "S|Warrior|7|1|Base,Arch|0|0|/schedule/6",
            "S|Warrior|8|1|Base,Arch|0|1|/schedule/7",
            "S|Warrior|9|1|Arch|0|0|/schedule/8",
            "S|Warrior|10|2|Hero|1|0|/schedule/9",
            "S|Warrior|11|1|Base,Arch|0|0|/schedule/10",
            "S|Warrior|12|1|Hero|0|1|/schedule/11",
            "S|Warrior|13|1|Base,Arch|0|0|/schedule/12",
            "S|Warrior|14|1|Hero|0|0|/schedule/13",
            "S|Warrior|15|1|Base,Arch|0|0|/schedule/14",
            "S|Warrior|16|1|Hero|0|1|/schedule/15",
            "S|Warrior|17|1|Base,Arch|0|0|/schedule/16",
            "S|Warrior|18|1|Hero|0|0|/schedule/17",
            "S|Warrior|19|1|Base,Arch|0|1|/schedule/18",
            "S|Warrior|20|0|-|0|0|/schedule/19",
            "S|Wizard|1|4|Base|2|0|/schedule/0",
            "S|Wizard|2|2|Base|0|0|/schedule/1",
            "S|Wizard|3|2|Arch|1|0|/schedule/2",
            "S|Wizard|4|1|Base,Arch|0|1|/schedule/3",
            "S|Wizard|5|1|Arch|0|0|/schedule/4",
            "S|Wizard|6|1|Base,Arch|0|0|/schedule/5",
            "S|Wizard|7|1|Arch|0|0|/schedule/6",
            "S|Wizard|8|1|Base,Arch|0|1|/schedule/7",
            "S|Wizard|9|1|Arch|0|0|/schedule/8",
            "S|Wizard|10|2|Hero|1|0|/schedule/9",
            "S|Wizard|11|1|Base,Arch|0|0|/schedule/10",
            "S|Wizard|12|1|Hero|0|1|/schedule/11",
            "S|Wizard|13|1|Base,Arch|0|0|/schedule/12",
            "S|Wizard|14|1|Hero|0|0|/schedule/13",
            "S|Wizard|15|1|Base,Arch|0|0|/schedule/14",
            "S|Wizard|16|1|Hero|0|1|/schedule/15",
            "S|Wizard|17|1|Base,Arch|0|0|/schedule/16",
            "S|Wizard|18|1|Hero|0|0|/schedule/17",
            "S|Wizard|19|1|Base,Arch|0|1|/schedule/18",
            "S|Wizard|20|0|-|0|0|/schedule/19"
        };
        private static readonly ReadOnlyCollection<ClassAdvancementScheduleRow> rows;
        private static readonly ReadOnlyCollection<ClassAdvancementSourceBinding> sources;
        private static readonly Dictionary<string,ClassAdvancementScheduleRow> byClassLevel;
        public static ReadOnlyCollection<ClassAdvancementScheduleRow> Rows=>rows;
        public static ReadOnlyCollection<ClassAdvancementSourceBinding> Sources=>sources;
        static ClassAdvancementScheduleCatalog()
        {
            var sourceRows=SourceFilesData.Split(new[]{';'},StringSplitOptions.RemoveEmptyEntries);
            var files=sourceRows.Select(x=>x.Split('|' )).Select(x=>new ClassAdvancementSourceBinding(x[0],x[1],x[2],x[3],x[4])).ToArray();
            if(files.Length!=17||files.Select(x=>x.ClassName).Distinct(StringComparer.Ordinal).Count()!=files.Length)
                throw new InvalidOperationException("Class advancement catalog requires the complete pinned 17-class manifest.");
            var fileMap=files.ToDictionary(x=>x.ClassName,StringComparer.Ordinal);
            var values=new List<ClassAdvancementScheduleRow>(EncodedRows.Length);
            foreach(string line in EncodedRows) {
                var f=line.Split('|');
                if(f[0]=="S") {
                    var bands=f[4]=="-"?Array.Empty<string>():f[4].Split(',');
                    values.Add(new ClassAdvancementScheduleRow(f[1],int.Parse(f[2],CultureInfo.InvariantCulture),ClassAdvancementScheduleKind.Structured,
                        int.Parse(f[3],CultureInfo.InvariantCulture),bands,int.Parse(f[5],CultureInfo.InvariantCulture),f[6]=="1",fileMap[f[1]].Path,f[7]));
                } else if(f[0]=="E") {
                    values.Add(new ClassAdvancementScheduleRow(f[1],int.Parse(f[2],CultureInfo.InvariantCulture),ClassAdvancementScheduleKind.NarrativeException,
                        null,Array.Empty<string>(),null,null,fileMap[f[1]].Path,f[3]));
                } else throw new InvalidOperationException("Unknown encoded schedule row.");
            }
            if(values.Count!=340||values.Select(x=>x.ClassName+"|"+x.ClassLevel.ToString(CultureInfo.InvariantCulture)).Distinct(StringComparer.Ordinal).Count()!=values.Count
                ||files.Count(x=>values.Count(r=>r.ClassName==x.ClassName)==20)!=17
                ||values.Count(x=>x.Kind==ClassAdvancementScheduleKind.Structured)!=280
                ||values.Count(x=>x.Kind==ClassAdvancementScheduleKind.NarrativeException)!=60)
                throw new InvalidOperationException("Class advancement catalog is incomplete or contains duplicate rows.");
            rows=Array.AsReadOnly(values.ToArray());sources=Array.AsReadOnly(files);
            byClassLevel=values.ToDictionary(x=>x.ClassName+"|"+x.ClassLevel.ToString(CultureInfo.InvariantCulture),StringComparer.Ordinal);
        }
        public static ClassAdvancementScheduleRow Get(string className,int classLevel)
        {
            if(className==null)throw new ArgumentNullException(nameof(className));
            return byClassLevel.TryGetValue(className+"|"+classLevel.ToString(CultureInfo.InvariantCulture),out var row)?row:null;
        }
        public static ClassAdvancementSourceBinding GetSource(string className)
        {
            if(className==null)throw new ArgumentNullException(nameof(className));
            return sources.SingleOrDefault(x=>x.ClassName==className);
        }
    }

    public sealed class ClassAdvancementSourceBinding
    {
        public string ClassName { get; }
        public string Path { get; }
        public string Sha256 { get; }
        public string GitBlobId { get; }
        public string DesignStatus { get; }
        internal ClassAdvancementSourceBinding(string className,string path,string sha256,string gitBlobId,string designStatus)
        {
            if(string.IsNullOrEmpty(className)||string.IsNullOrEmpty(path)||sha256==null||sha256.Length!=64
                ||gitBlobId==null||gitBlobId.Length!=40||string.IsNullOrEmpty(designStatus))
                throw new ArgumentException("Invalid class advancement source binding.");
            ClassName=className;Path=path;Sha256=sha256;GitBlobId=gitBlobId;DesignStatus=designStatus;
        }
    }
}
