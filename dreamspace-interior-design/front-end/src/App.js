// import logo from './logo.svg';
// import './App.css';
// function App() {
//   return (
//     <div className="App">
//       <header className="App-header">
//         <img src={logo} className="App-logo" alt="logo" />
//         <p>
//           Edit <code>src/App.js</code> and save to reload.
//         </p>
//         <a
//           className="App-link"
//           href="https://reactjs.org"
//           target="_blank"
//           rel="noopener noreferrer"
//         >
//           Learn React
//         </a>
//       </header>
//     </div>
//   );
// }
// export default App;

// frontend/src/App.js
import React from 'react';
import UserRegistration from './components/UserRegistration';

const App = () => {
  return (
    <div>
      <h1>DreamSpace: Interior Design</h1>
      <UserRegistration />
    </div>
  );
};

export default App;
