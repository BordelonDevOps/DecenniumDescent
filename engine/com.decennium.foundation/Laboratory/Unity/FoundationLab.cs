#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD)
using System;
using System.IO;
using System.Linq;
using UnityEngine;
using UnityEngine.UIElements;

namespace Decennium.Foundation.Laboratory
{
    [RequireComponent(typeof(UIDocument))]
    public sealed class FoundationLab : MonoBehaviour
    {
        [SerializeField] private StyleSheet laboratoryStyle;
        [SerializeField] private Font laboratoryFont;
        private Simulation simulation;
        private VisualElement root, panel, commands;
        private Label stateLabel, resultLabel;
        private Sprite square;
        private GameObject visuals;
        private Transform actorView, companionView;
        private SpriteRenderer containerView;
        private bool started;
        private string startupMessage = "TEST_ONLY fixture. No production movement, reward or time rules.";
        public string SavePath => Path.Combine(Application.persistentDataPath, "DecenniumTestOnly", "foundation.ddsave");

        public void Configure(StyleSheet style, Font font) { laboratoryStyle = style; laboratoryFont = font; }
        private void OnEnable()
        {
            if (simulation == null)
            {
                try { RestoreOrCreate(); }
                catch (Exception error) { startupMessage = "LOAD BLOCKED: " + error.Message + " Use Recover primary from backup. A new in-memory fixture does not repair disk corruption."; }
            }
            CreateViews();
            if (started) BindUi();
        }
        private void Start() { started = true; BindUi(); }
        private void RestoreOrCreate()
        {
            var policy = new TestOnlyPolicy();
            var snapshot = File.Exists(SavePath) ? new FileSaveStore().Load(SavePath) : policy.Initial();
            simulation = new Simulation(policy, snapshot, ExecutionProfile.Laboratory);
        }
        private void BindUi()
        {
            if (panel != null) return;
            root = GetComponent<UIDocument>().rootVisualElement;
            if (root == null) { Debug.LogError("TEST_ONLY lab requires an enabled UIDocument and PanelSettings."); return; }
            if (laboratoryStyle != null) root.styleSheets.Add(laboratoryStyle);
            if (laboratoryFont != null) root.style.unityFont = laboratoryFont;
            panel = new VisualElement(); panel.AddToClassList("lab-panel"); root.Add(panel);
            panel.Add(new Label("DECENNIUM FOUNDATION — TEST_ONLY") { name = "labHeading" });
            panel.Add(new Label("Manual command laboratory. Coordinates and ticks have no game-world units.") { name = "labDescription" });
            stateLabel = new Label(); stateLabel.AddToClassList("lab-state"); panel.Add(stateLabel);
            commands = new VisualElement(); panel.Add(commands);
            var movement = new VisualElement(); movement.AddToClassList("lab-row"); commands.Add(movement);
            Button(movement,"Left",()=>Move(-1,0)); Button(movement,"Up",()=>Move(0,1));
            Button(movement,"Down",()=>Move(0,-1)); Button(movement,"Right",()=>Move(1,0));
            Button(commands,"Open TEST_ONLY container",()=>Send(CommandKind.Interact,TestOnlyPolicy.ContainerId));
            Button(commands,"Advance one TEST_ONLY tick",()=>Send(CommandKind.AdvanceClock,x:1));
            Button(commands,"Save fixture",()=>Attempt(()=>new FileSaveStore().Save(SavePath,simulation.Capture()),"Saved: "+SavePath));
            Button(panel,"Load fixture",()=>Load(SavePath));
            Button(panel,"Recover primary from backup (preserves old primary)",RecoverBackup);
            Button(panel,"Start new TEST_ONLY fixture (keeps disk save)",()=>{
                simulation=new Simulation(new TestOnlyPolicy(),new TestOnlyPolicy().Initial(),ExecutionProfile.Laboratory);
                Show("New in-memory fixture. Existing disk save retained until Save."); });
            resultLabel=new Label(startupMessage);resultLabel.AddToClassList("lab-result");panel.Add(resultLabel);
            panel.Add(new Label("Blue: actor · Orange: companion · Gold: container · Gray: wall"));
            Refresh();
        }
        private static void Button(VisualElement parent,string text,Action callback)
        { var button=new Button(callback){text=text};parent.Add(button); }
        private void Move(int x,int y) => Send(CommandKind.Move,x:x,y:y);
        private void Send(CommandKind kind,string target="",int x=0,int y=0)
        {
            if(simulation==null) return;
            var command=new Command(Guid.NewGuid().ToString("N"),TestOnlyPolicy.ActorId,simulation.Capture().Revision,kind,target,x,y);
            var result=simulation.Execute(TestOnlyPolicy.Host(),command);
            Show(result.Outcome+": "+result.Code);
        }
        private void Load(string path) => Attempt(()=>{
            var candidate=new Simulation(new TestOnlyPolicy(),new FileSaveStore().Load(path),ExecutionProfile.Laboratory);
            simulation=candidate;
        },"Loaded: "+path);
        private void RecoverBackup()
        {
            try {
                Simulation candidate=null;
                string preserved=new FileSaveStore().RecoverBackup(SavePath,snapshot=>
                    candidate=new Simulation(new TestOnlyPolicy(),snapshot,ExecutionProfile.Laboratory));
                simulation=candidate;
                Show("Recovered backup to primary. Backup retained. "+(preserved==null?"No previous primary.":"Previous primary: "+preserved));
            }
            catch(Exception error) {Show("RECOVERY BLOCKED: "+error.Message);Debug.LogWarning(error.ToString());}
        }
        private void Attempt(Action action,string message)
        {
            try {action();Show(message);}
            catch(Exception error) {Show("BLOCKED: "+error.Message);Debug.LogWarning(error.ToString());}
        }
        private void Show(string text) {if(resultLabel!=null)resultLabel.text=text;Refresh();}
        private void Refresh()
        {
            if(commands!=null)commands.SetEnabled(simulation!=null);
            if(simulation==null){if(stateLabel!=null)stateLabel.text="No state loaded.";return;}
            var state=simulation.Capture();var actor=state.Actors.Single(a=>a.Id==TestOnlyPolicy.ActorId);
            var companion=state.Actors.Single(a=>a.Id==TestOnlyPolicy.CompanionId);
            if(actorView!=null)actorView.position=new Vector3(actor.X,actor.Y,-0.2f);
            if(companionView!=null)companionView.position=new Vector3(companion.X,companion.Y,-0.2f);
            if(containerView!=null)containerView.color=state.Objects[0].Opened?new Color(0.45f,0.35f,0.1f):new Color(1f,0.8f,0.2f);
            if(stateLabel!=null)stateLabel.text="Revision "+state.Revision+" · Tick "+state.Clock+"\nActor ("+actor.X+", "+actor.Y+") · Tokens "+actor.Tokens;
        }
        private void CreateViews()
        {
            square=Sprite.Create(Texture2D.whiteTexture,new Rect(0,0,Texture2D.whiteTexture.width,Texture2D.whiteTexture.height),new Vector2(0.5f,0.5f),Texture2D.whiteTexture.width);
            visuals=new GameObject("TEST_ONLY_Views");visuals.transform.SetParent(transform,false);
            for(int x=0;x<5;x++)for(int y=0;y<5;y++)MakeSquare("TEST_ONLY_tile",x,y,1,TestOnlyPolicy.Walkable(x,y)?new Color(0.13f,0.19f,0.22f):Color.gray,0.94f);
            actorView=MakeSquare("TEST_ONLY_actor",1,1,-0.2f,new Color(0.25f,0.65f,1f),0.6f).transform;
            companionView=MakeSquare("TEST_ONLY_companion",3,3,-0.2f,new Color(1f,0.45f,0.15f),0.6f).transform;
            containerView=MakeSquare("TEST_ONLY_container",1,2,0,new Color(1f,0.8f,0.2f),0.7f);
        }
        private SpriteRenderer MakeSquare(string label,int x,int y,float z,Color color,float size)
        {
            var go=new GameObject(label);go.transform.SetParent(visuals.transform,false);go.transform.position=new Vector3(x,y,z);
            go.transform.localScale=Vector3.one*size;var renderer=go.AddComponent<SpriteRenderer>();renderer.sprite=square;renderer.color=color;return renderer;
        }
        private void OnDisable()
        {
            if(panel!=null)panel.RemoveFromHierarchy();panel=null;commands=null;stateLabel=null;resultLabel=null;
            if(root!=null && laboratoryStyle!=null)root.styleSheets.Remove(laboratoryStyle);root=null;
            if(visuals!=null)Destroy(visuals);if(square!=null)Destroy(square);
            visuals=null;square=null;actorView=null;companionView=null;containerView=null;
        }
    }
}
#endif
