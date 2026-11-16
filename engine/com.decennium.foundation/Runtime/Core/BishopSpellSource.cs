// Exact immutable source projection for the separately admitted earned3 spell. No casting authority is implied.
namespace Decennium.Foundation
{
    public static partial class BishopProfile
    {
        public static SpellSourceDefinition DispelSource { get; } = new SpellSourceDefinition("dispel-magic-lesser", "Dispel Magic (Lesser)", "/spells/33", "dafda6181f1f01bc2dfe2c045dbad6029dadb7faf21d15f09426c2f1f0c39812", "9765464cf9dfd90ce6f5d40d1157605477a025cfbca511f8f29fe7868473aff5", "a6d6134c38f81470bf836d5d193a8d13b836607e5834eecfd71bb24f6ea96553", "00b8ca984885865fce7331965a38fba94c8ae31709e54247c5824a1ea6e6b38b", 0,
            new[] {
                new SpellClassAccess("Cleric", "Abjuration", 2, 3, 3),
                new SpellClassAccess("Druid", "Abjuration", 2, 3, 3),
                new SpellClassAccess("Mage", "Abjuration", 2, 3, 3),
                new SpellClassAccess("Monk", "Abjuration", 2, 8, 3),
                new SpellClassAccess("Paladin", "Abjuration", 2, 5, 3),
                new SpellClassAccess("Tinker", "Abjuration", 2, 6, 3),
                new SpellClassAccess("Wizard", "Abjuration", 2, 3, 3)
            }, new[] {
                new SpellSourcePlacement("Abjuration", 2, "End magical effects of 2nd level or lower.")
            });
    }
}
