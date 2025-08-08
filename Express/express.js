import express from "express";

const app=express();
import path from 'path'
import { fileURLToPath } from 'url';
// Setup __dirname for ES modules
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Middleware
app.use(express.urlencoded({ extended: true }));
app.use(express.static(path.join(__dirname, 'public')));

app.use(express.json());
const port=3000;

app.use(express.json());
app.get('/page',(req,res)=>{
    res.send("Gurram")
});
 app.get('/page1',(req,res)=>{
    res.send("FutureDealer")

});
app.post('/submit',(req,res)=>{
    const {name,email}=req.body;
    res.send(`Hello ${name},(${email}) post is done`)
});
app.listen(port,()=>{
    console.log(`live server http://localhost:${port}/form.html`);
});