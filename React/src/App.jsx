
import React from "react"; 
import "./App.css";
function App() {
  return (
      <div className="container">
        <h1>E-COMMERCE</h1>
        <section className="Products">
            <div className="card">
              <img src="Buds2-Pro-Purple-EEZEPC-1.jpg" alt="Import Product" />
              <p>Samsung Galaxy Buds 2 Pro</p>
              <p>price:5999/-</p>
              <button>Add to cart</button>
              </div>
              <div className="card1">
              <img src="Flip.jpg" alt="Import Product" />
               <p>Samsung Galaxy z-Flip 4</p>
              <p>price:99999/-</p>
              <button>Add to cart</button>
              </div>
              <div className="card2">
              <img src="Fold.webp" alt="Import Product" />
               <p>Samsung Galaxy Fold 5</p>
              <p>price:215999/-</p>
              <button>Add to cart</button>
            </div>

        </section>
      </div>
  );
}

export default App;
