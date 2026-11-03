using System;
using System.Linq;
using UnityEditor;
using UnityEditor.Build;
using UnityEditor.Build.Reporting;
using UnityEngine.SceneManagement;

namespace Decennium.Foundation.EditorTools
{
    public sealed class LaboratoryGate : IPreprocessBuildWithReport, IProcessSceneWithReport
    {
        public int callbackOrder => -10000;
        [MenuItem("Decennium/TEST_ONLY/Enable laboratory for active target")]
        public static void Enable()
        {
            var target=NamedBuildTarget.FromBuildTargetGroup(EditorUserBuildSettings.selectedBuildTargetGroup);
            string[] symbols=PlayerSettings.GetScriptingDefineSymbols(target).Split(';');
            if(!symbols.Contains("DECENNIUM_TEST_ONLY"))
                PlayerSettings.SetScriptingDefineSymbols(target,string.Join(";",symbols.Where(s=>!string.IsNullOrEmpty(s)).Concat(new[]{"DECENNIUM_TEST_ONLY"})));
        }
        public void OnPreprocessBuild(BuildReport report)
        {
            if((report.summary.options & BuildOptions.Development)!=0)return;
            var target=NamedBuildTarget.FromBuildTargetGroup(BuildPipeline.GetBuildTargetGroup(report.summary.platform));
            if(PlayerSettings.GetScriptingDefineSymbols(target).Split(';').Contains("DECENNIUM_TEST_ONLY"))
                throw new BuildFailedException("Remove DECENNIUM_TEST_ONLY from the release target. Laboratory content is not release content.");
        }
        public void OnProcessScene(Scene scene,BuildReport report)
        {
            if(report==null || (report.summary.options & BuildOptions.Development)!=0)return;
            if(scene.path.Contains("/DecenniumTestOnly/") || scene.GetRootGameObjects().Any(go=>go.name.StartsWith("TEST_ONLY",StringComparison.Ordinal)))
                throw new BuildFailedException("TEST_ONLY scene detected in release build: "+scene.path);
        }
    }
}
