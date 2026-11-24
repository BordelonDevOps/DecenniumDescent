#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System.Runtime.CompilerServices;

[assembly: InternalsVisibleTo("Decennium.Foundation.LabModel")]
#endif
