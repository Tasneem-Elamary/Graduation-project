import { Schema, model } from 'mongoose'

const userSchema = new Schema({
   identifier: { type: Number, 
        required: [true, 'id is required'] ,
        unique:true },
    
    age: { type: Number,
         required: [true, 'age is required']
         },

    gender: {
        type: String,
        default: "Male",
        enum: ['Male', 'Female']
    },
    comments:{
    type: String,
    },
    phone:{
        type: String,
        required: [true, 'phone is required']
        },
    Email:{
        type: String,
        required: [true, 'email is required']
        },
    originalimage: {
        type: String,
        required: [true, 'image is required']
    },
    grade:{
        type: String,
    },
    hardEXimage:{
        type: String,
    },
    softEXimage:{
        type: String,
    },
    microimage:{
        type: String,
    },
    hemoimage:{
        type: String,
    },
   
    
   
}, {
    timestamps: true
})

export const userModel  =  model('User', userSchema)