//IMPORT LIBRARIES
import {
  AmbientLight,
  BoxGeometry,
  AxesHelper,
  DirectionalLight,
  GridHelper,
  Material,
  MeshBasicMaterial,
  PerspectiveCamera,
  Scene,
  WebGLRenderer,
  Raycaster,
  Vector2,
  LineStrip,
} from "three"; //3D rendering
import { IFCSPACE } from "web-ifc"; //IFC
import { IFCLoader } from "web-ifc-three/IFCLoader"; //IFC
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls.js"; //orbit
import { MeshLambertMaterial } from "three"; //mesh
import { Mesh } from "three";
import {
  acceleratedRaycast,
  computeBoundsTree,
  disposeBoundsTree,
} from "three-mesh-bvh"; ///Raycasting

// THREE SCENE
//Creates the Three.js scene
const scene = new Scene();
//Object to store the size of the viewport
const size = {
  width: window.innerWidth,
  height: window.innerHeight,
};
//Creates the camera (point of view of the user)
const camera = new PerspectiveCamera(75, size.width / size.height);
camera.position.z = 20;
camera.position.y = 10;
camera.position.x = 0;
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

//SELECTION

//Sets up the IFC loading
const ifcModels = [];
const ifcLoader = new IFCLoader();
const ifcUrl = "../static/IFCSample_School.ifc";
async function loadIFC() {
  await ifcLoader.ifcManager.setWasmPath("../../IFCViewer/wasm_wit/");
  const model = await ifcLoader.loadAsync(ifcUrl);
  scene.add(model);
  ifcModels.push(model);
}
loadIFC()

// Sets up optimized picking
ifcLoader.ifcManager.setupThreeMeshBVH(
  computeBoundsTree,
  disposeBoundsTree,
  acceleratedRaycast
);

const raycaster = new Raycaster();
raycaster.firstHitOnly = true;
const mouse = new Vector2();

function cast(event) {
  // Computes the position of the mouse on the screen
  const bounds = threeCanvas.getBoundingClientRect();

  const x1 = event.clientX - bounds.left;
  const x2 = bounds.right - bounds.left;
  mouse.x = (x1 / x2) * 2 - 1;

  const y1 = event.clientY - bounds.top;
  const y2 = bounds.bottom - bounds.top;
  mouse.y = -(y1 / y2) * 2 + 1;

  // Places it on the camera pointing to the mouse
  raycaster.setFromCamera(mouse, camera);

  // Casts a ray
  return raycaster.intersectObjects(ifcModels);
}

const output_id = document.getElementById("id-output");
const output_category = document.getElementById("type-output");

function pick(event) {
  const found = cast(event)[0];
  if (found) {
    const index = found.faceIndex;
    const geometry = found.object.geometry;
    const ifc = ifcLoader.ifcManager;
    const id = ifc.getExpressId(geometry, index);
    const type = ifc.getIfcType(0, id);

    output_id.innerHTML = id;
    output_category.innerHTML = type;
  }
}

window.ondblclick = pick;



