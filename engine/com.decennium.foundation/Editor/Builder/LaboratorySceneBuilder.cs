#if DECENNIUM_TEST_ONLY
using System;
using System.IO;
using Decennium.Foundation.Laboratory;
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEngine;
using UnityEngine.UIElements;

namespace Decennium.Foundation.EditorTools
{
    public static class LaboratorySceneBuilder
    {
        public const string ScenePath="Assets/DecenniumTestOnly/FoundationLab.unity";
        [MenuItem("Decennium/TEST_ONLY/Create or open foundation laboratory")]
        public static void CreateOrOpen()
        {
            if(Application.isPlaying)throw new InvalidOperationException("Exit Play Mode before creating a scene.");
            if(!EditorSceneManager.SaveCurrentModifiedScenesIfUserWantsTo())return;
            if(File.Exists(ScenePath)) {EditorSceneManager.OpenScene(ScenePath);return;}
            const string directory="Assets/DecenniumTestOnly";
            if(!AssetDatabase.IsValidFolder(directory))AssetDatabase.CreateFolder("Assets","DecenniumTestOnly");
            var style=AssetDatabase.LoadAssetAtPath<StyleSheet>("Packages/com.decennium.foundation/Laboratory/Unity/Laboratory.uss");
            if(style==null)throw new InvalidOperationException("Laboratory stylesheet not imported. Fix import errors before building the scene.");
            const string panelPath=directory+"/LaboratoryPanel.asset";
            var settings=AssetDatabase.LoadAssetAtPath<PanelSettings>(panelPath);
            if(settings==null)
            {
                if(File.Exists(panelPath))throw new InvalidOperationException("Panel asset exists with an incompatible type; preserved.");
                settings=ScriptableObject.CreateInstance<PanelSettings>();settings.scaleMode=PanelScaleMode.ScaleWithScreenSize;
                settings.referenceResolution=new Vector2Int(1280,720);AssetDatabase.CreateAsset(settings,panelPath);
            }
            var scene=EditorSceneManager.NewScene(NewSceneSetup.EmptyScene,NewSceneMode.Single);
            var cameraObject=new GameObject("TEST_ONLY_Camera");var camera=cameraObject.AddComponent<Camera>();
            camera.orthographic=true;camera.orthographicSize=4f;camera.transform.position=new Vector3(0.6f,2f,-10f);
            camera.clearFlags=CameraClearFlags.SolidColor;camera.backgroundColor=new Color(0.05f,0.07f,0.09f);
            var laboratory=new GameObject("TEST_ONLY_Foundation");var document=laboratory.AddComponent<UIDocument>();document.panelSettings=settings;
            laboratory.AddComponent<FoundationLab>().Configure(style,Resources.GetBuiltinResource<Font>("LegacyRuntime.ttf"));
            EditorSceneManager.MarkSceneDirty(scene);
            if(!EditorSceneManager.SaveScene(scene,ScenePath))throw new IOException("Could not save the laboratory scene.");
            AssetDatabase.SaveAssets();Selection.activeGameObject=laboratory;
            Debug.Log("Created TEST_ONLY laboratory. Press Play. This does not verify compilation, gameplay or a build.");
        }
    }
}
#endif
