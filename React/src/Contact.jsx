import React from "react";

function Contact(){
    return(
        <div>
            <form>
                <input type="text"placeholder="Username"></input><br></br>
                <input type="email"placeholder="email"></input><br></br>
                <input type="tel"placeholder="contact"></input><br></br>
                <textarea placeholder="message here"></textarea><br></br>
                <button type="submit">confirm</button>
            </form>
        </div>
    );
}
export default Contact;