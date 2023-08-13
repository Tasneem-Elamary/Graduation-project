import joi from 'joi'

export const postinfo = {
    body: joi.object().required().keys({
        identifier: joi.number().integer().required() ,
        age : joi.number().integer().required() ,
        comments: joi.string(),
        gender : joi.string().required(),
        phone: joi.string(),
        Email: joi.string(),    
    }),

    
}



export const getpatientbyid = {
    params:joi.object().required().keys({
        id:joi.string().required()
    }),
    
}
