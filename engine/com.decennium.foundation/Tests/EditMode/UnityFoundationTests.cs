#if UNITY_EDITOR && DECENNIUM_TEST_ONLY && UNITY_INCLUDE_TESTS
using System;
using System.IO;
using NUnit.Framework;

namespace Decennium.Foundation.Tests
{
    public sealed class UnityFoundationTests
    {
        public static string[] Cases => FoundationCases.Names();
        [TestCaseSource(nameof(Cases))]
        public void SharedRegression(string name)
        {
            string output=Path.Combine(Path.GetTempPath(),"DecenniumTestOnly",Guid.NewGuid().ToString("N"));
            var result=FoundationCases.Run(name,output);
            Assert.That(result.Passed,Is.True,result.Error);
        }
    }
}
#endif
