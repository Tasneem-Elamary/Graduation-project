
import { userModel } from "../DB/models/user.model.js"
import cloudinary from "../service/cloudinary.js";
import axios from 'axios'


export const postInfo=async(req,res)=>{
    try {
     
        if (!req.file) {
           res.json({ message: "Please upload u image" })
        } else {
          
            const {secure_url,public_id,folder} = await cloudinary.uploader.upload(req.file.path, {
                folder: `retinopathy/${req.body.identifier}`
            })
            
            
            req.body.originalimage=secure_url
            console.log(secure_url)
        
            
            await axios.post('http://127.0.0.1:5000/grade',JSON.stringify({originalimage:secure_url}))
             .then(async function (response) {
              // handle success
             // console.log(response.data.prediction);
              req.body.grade=response.data.grade
              
            }).catch(function (error) {
              // handle error
                console.log(error);
            })
        
            // await axios.post('http://127.0.0.1:5000/hardExudates',JSON.stringify({originalimage:secure_url,identifier:req.body.identifier}))
            // .then(async function (response) {
            //   // handle success
            //   //console.log(response.data.prediction);
            //   req.body.hardEXimage=response.data.resultimage
              
            // })
            // .catch(function (error) {
            //   // handle error
            // console.log(error);
            // })

            // await axios.post('http://127.0.0.1:5000/Micro',JSON.stringify({originalimage:secure_url,identifier:req.body.identifier}))
            // .then(async function (response) {

            //   req.body.microimage=response.data.resultimage
              
            // })
            // .catch(function (error) {
            //   // handle error
            // console.log(error);
            // })

            // await axios.post('http://127.0.0.1:5000/softExudates',JSON.stringify({originalimage:secure_url,identifier:req.body.identifier}))
            // .then(async function (response) {

            //   req.body.softEXimage=response.data.resultimage
              
            // })
            // .catch(function (error) {
            //   // handle error
            // console.log(error);
            // })

            // await axios.post('http://127.0.0.1:5000/hemorrage',JSON.stringify({originalimage:secure_url,identifier:req.body.identifier}))
            // .then(async function (response) {

            //   req.body.hemoimage=response.data.resultimage
              
            // })
            // .catch(function (error) {
            //   // handle error
            // console.log(error);
            // })

            const newUser = new userModel(req.body)
            const savedUser = await newUser.save()
            res.status(200).json({ message: "Done", savedUser })
            console.log(['message'])
        }
        
    } catch (error) {
       return  res.status(500).json({ message: "catch error",error: error.message })
    }
    
}

export const getPatientsInfo=async(req,res)=>{
   
          const users=await userModel.find({}).select("-_id identifier age gender comments originalimage createdAt")
           return  res.status(200).json({ message: "Done", users })
        

}

export const getpatientById=async(req,res)=>{
    const{id}=req.params
    //console.log(req.params);
    const user=await userModel.findOne({identifier:id}).select("-_id identifier age gender comments grade createdAt phone Email originalimage hardEXimage microimage softEXimage hemoimage")
    
   res.status(200).json({ message: "Done", user })
  }

export const getHardEXpic=async(req,res)=>{
  const{id}=req.params
  const user=await userModel.findOne({identifier:id}).select("-_id hardEXimage ")
  return res.status(200).json({ message: "Done", user })
}


export const postHardEXpic=async(req,res)=>{
    const{id}=req.params
    const {originalimage,identifier}=await userModel.findOne({identifier:id}).select("-_id originalimage identifier")
    //console.log(JSON.stringify({originalimage,identifier}));
    axios.post('http://127.0.0.1:5000/hardExudates',JSON.stringify({originalimage,identifier}))
  .then(async function (response) {
    // handle success
    //console.log(response.data.prediction);
    const updateduser=await userModel.findOneAndUpdate({identifier:id},{hardEXimage:response.data.resultimage},{new:true})
    res.status(200).json({ message: "Done" })
  })
  .catch(function (error) {
    // handle error
   console.log(error);
  })
  
  }

  



export const deletePatient=async(req,res)=>{
    const{id}=req.params
    const user=await userModel.findOneAndDelete({identifier:id})
    
    if(user){
      
       return res.status(200).json({ message: "Done", user })
    }
    else{
       return res.status(400).json({ message: "in-valid id" })
    }
}



export const updatePatient=async(req,res)=>{
    const{id}=req.params
    const user=await userModel.updateOne({identifier:id},req.body)
    if(user.modifiedCount){
        return res.status(200).json({ message: "Done", user })
    }
    else{
       return  res.status(400).json({ message: "in-valid id" })
    }
}
 
 