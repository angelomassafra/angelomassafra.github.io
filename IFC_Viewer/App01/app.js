//SIMPLE IFC VIEWER WITH PICKING AND HIGHLIGHTING

//////////////////////////////////////////////////////////////////////////////////////////////////
//00 - IMPORT LIBRARIES
import {
  AmbientLight,
  AxesHelper,
  DirectionalLight,
  GridHelper,
  PerspectiveCamera,
  Scene,
  WebGLRenderer,
  Raycaster,
  Vector2,
} from "three"; //Three.js
import { IFCLoader } from "web-ifc-three/IFCLoader"; //IFC
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls.js"; //orbit
import { MeshLambertMaterial } from "three"; //mesh
import {
  acceleratedRaycast,
  computeBoundsTree,
  disposeBoundsTree,
} from "three-mesh-bvh"; ///Raycasting

//////////////////////////////////////////////////////////////////////////////////////////////////
//01 - HELPER FUNCTIONS
// Casting
function cast(event) {
  const bounds = threeCanvas.getBoundingClientRect();
  const x1 = event.clientX - bounds.left;
  const x2 = bounds.right - bounds.left;
  mouse.x = (x1 / x2) * 2 - 1;
  const y1 = event.clientY - bounds.top;
  const y2 = bounds.bottom - bounds.top;
  mouse.y = -(y1 / y2) * 2 + 1;
  raycaster.setFromCamera(mouse, camera);
  return raycaster.intersectObjects(ifcModels);
}
// Picking
function pick(event) {
  const found = cast(event)[0];
  if (found) {
    const index = found.faceIndex;
    const geometry = found.object.geometry;
    const id = ifc.getExpressId(geometry, index); // Get IFC ID
    const type = ifc.getIfcType(0, id); //Get IFC Category

    output_id.innerHTML = id;
    output_category.innerHTML = type;
  }
}
// Highlightin
function highlight(event, material, model, threeCanvas, camera, scene) {
  const found = cast(event, threeCanvas, camera)[0];
  if (found) {
    // Gets model ID
    model.id = found.object.modelID;
    // Gets Express ID
    const index = found.faceIndex;
    const geometry = found.object.geometry;
    const id = ifc.getExpressId(geometry, index);
    // Creates subset
    ifc.createSubset({
      modelID: model.id,
      ids: [id],
      material: material,
      scene: scene,
      removePrevious: true,
    });
  } else {
    // Removes previous highlight
    ifc.removeSubset(model.id, material);
  }
}

//////////////////////////////////////////////////////////////////////////////////////////////////
//02 - SETUP INPUTS
const ifcUrl = "IFCSample_HomeMaker.ifc";
const wasmPath = "../../IFC_Viewer/wasm_wit/";

const cameraPositionZ = 20;
const cameraPositionY = 10;
const cameraPositionX = 0;

//////////////////////////////////////////////////////////////////////////////////////////////////
//03 - SETUP THREE SCENE
//Creates the Three.js scene
const scene = new Scene();
//Object to store the size of the viewport
const size = {
  width: window.innerWidth,
  height: window.innerHeight,
};
//Creates the camera (point of view of the user)
const camera = new PerspectiveCamera(75, size.width / size.height);
camera.position.z = cameraPositionZ;
camera.position.y = cameraPositionY;
camera.position.x = cameraPositionX;
//Creates the lights of the scene
const lightColor = 0xffffff;
const ambientLight = new AmbientLight(lightColor, 0.5);
scene.add(ambientLight);
const directionalLight = new DirectionalLight(lightColor, 1);
directionalLight.position.set(0, 10, 0);
directionalLight.target.position.set(-5, 0, 0);
scene.add(directionalLight);
scene.add(directionalLight.target);
//Sets up the renderer, fetching the canvas of the HTML
const threeCanvas = document.getElementById("three-canvas");
const renderer = new WebGLRenderer({ canvas: threeCanvas, alpha: true });
renderer.setSize(size.width, size.height);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
//Creates grids and axes in the scene
const grid = new GridHelper(50, 30);
scene.add(grid);
const axes = new AxesHelper();
axes.material.depthTest = false;
axes.renderOrder = 1;
scene.add(axes);
//Creates the orbit controls (to navigate the scene)
const controls = new OrbitControls(camera, threeCanvas);
controls.enableDamping = true;
controls.target.set(-2, 0, 0);
//Animation loop
const animate = () => {
  controls.update();
  renderer.render(scene, camera);
  requestAnimationFrame(animate);
};
animate();
//Adjust the viewport to the size of the browser
window.addEventListener("resize", () => {
  (size.width = window.innerWidth), (size.height = window.innerHeight);
  camera.aspect = size.width / size.height;
  camera.updateProjectionMatrix();
  renderer.setSize(size.width, size.height);
});

//////////////////////////////////////////////////////////////////////////////////////////////////
//04 - SETUP IFC LOADER
const ifcModels = [];
const ifcLoader = new IFCLoader();
const ifc = ifcLoader.ifcManager;

async function loadIFC() {
  await ifc.setWasmPath(wasmPath);
  const model = await ifcLoader.loadAsync(ifcUrl);
  scene.add(model);
  ifcModels.push(model);
}
loadIFC();

//////////////////////////////////////////////////////////////////////////////////////////////////
//05 - SETUP PICKER AND HIGHLIGHTER
// Sets up optimized picking
ifc.setupThreeMeshBVH(
  computeBoundsTree,
  disposeBoundsTree,
  acceleratedRaycast
);
// Set up raycasting
const raycaster = new Raycaster();
raycaster.firstHitOnly = true;
const mouse = new Vector2();
// Selection material
const selectMat = new MeshLambertMaterial({
  transparent: true,
  opacity: 1,
  color: 0x097dc1,
  depthTest: false,
});
// Reference to the previous selection
const selectModel = { id: -1 };
// Preselection material
const preselectMat = new MeshLambertMaterial({
  transparent: true,
  opacity: 0.5,
  color: 0x097dc1,
  depthTest: false,
});
// Reference to the previous selection
let preselectModel = { id: -1 };

//////////////////////////////////////////////////////////////////////////////////////////////////
//06 - HTML INTERACTION
// Output panel
const output_id = document.getElementById("id-output");
const output_category = document.getElementById("type-output");
window.ondblclick = pick;
// Preselection
threeCanvas.onmousemove = (event) =>
highlight(
  event,
  preselectMat,
  preselectModel,
  threeCanvas,
  camera,
  scene
);
// Selection
threeCanvas.ondblclick = (event) => {
  highlight(event, selectMat, selectModel, threeCanvas, camera, scene);
};


