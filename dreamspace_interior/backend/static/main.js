// Import the necessary modules
import * as THREE from "https://cdn.skypack.dev/three@0.129.0/build/three.module.js";
import { OrbitControls } from "https://cdn.skypack.dev/three@0.129.0/examples/jsm/controls/OrbitControls.js";
import { GLTFLoader } from "https://cdn.skypack.dev/three@0.129.0/examples/jsm/loaders/GLTFLoader.js";

// Create a Three.js scene, camera, and renderer
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({ alpha: true });
renderer.setSize(window.innerWidth, window.innerHeight);

// Append the renderer to the DOM
const canvasContainer = document.querySelector(".canvas-container");
canvasContainer.appendChild(renderer.domElement);

// Keep track of the mouse position
let mouseX = window.innerWidth / 2;
let mouseY = window.innerHeight / 2;

// Keep the 3D object on a global variable
let object;

// OrbitControls for camera movement
let controls;

// Set which object to render
let objToRender = 'bedroom_white';

// Instantiate a loader for the .gltf file
const loader = new GLTFLoader();

// Load the file
loader.load(
    `/static/models/${objToRender}/scene.gltf`,
    function (gltf) {
      // If the file is loaded, add it to the scene
      object = gltf.scene;
      scene.add(object);
  
      // Adjust the position of the bedroom_white model
      if (objToRender === "bedroom_white") {
        object.position.set(0, -5, 0); // You may need to adjust these values based on your model
      }
  
      console.log("Loaded");
    },
    function (xhr) {
      // While it is loading, log the progress
      console.log((xhr.loaded / xhr.total) * 100 + "% loaded");
    },
    function (error) {
      // If there is an error, log it
      console.error(error);
    }
);

// Set how far the camera will be from the 3D model
camera.position.z = objToRender === "bedroom_white" ? 25 : 500;

// Add lights to the scene
const topLight = new THREE.DirectionalLight(0xffffff, 5);
topLight.position.set(500, 500, 500);
topLight.castShadow = true;
scene.add(topLight);

const ambientLight = new THREE.AmbientLight(0x333333, objToRender === "bedroom_white" ? 10 : 1);
scene.add(ambientLight);

// Add OrbitControls to the camera
if (objToRender === "bedroom_white") {
  controls = new OrbitControls(camera, renderer.domElement);
}

// Render the scene
function animate() {
  requestAnimationFrame(animate);

  // Update the scene and handle mouse movement
  if (object && objToRender === "eye") {
    object.rotation.y = -3 + mouseX / window.innerWidth * 3;
    object.rotation.x = -1.2 + mouseY * 2.5 / window.innerHeight;
  }

  // Render the scene
  renderer.render(scene, camera);
}

// Add a listener for window resize
window.addEventListener("resize", function () {
    camera.aspect = canvasContainer.clientWidth / canvasContainer.clientHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(canvasContainer.clientWidth, canvasContainer.clientHeight);
  });

// Add a listener for mouse movement
document.onmousemove = (e) => {
  mouseX = e.clientX;
  mouseY = e.clientY;
}

// Append the renderer to the DOM
document.getElementById("container3D").appendChild(renderer.domElement);

// Start the 3D rendering
animate();
