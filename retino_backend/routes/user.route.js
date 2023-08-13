import { Router } from "express";
import {  deletePatient, getpatientById, getPatientsInfo,   postHardEXpic,   postInfo , updatePatient } from "../controllers/user.controller.js";
import { validation } from "../middleware/validation.js";
import { HME, myMulter, validationTypes } from "../service/clodMulter.js";
import { getpatientbyid, postinfo } from "../validators/user.validation.js";
const router = Router()


router.post("/",myMulter(validationTypes.iamge).single('image'),validation(postinfo),HME,postInfo)
router.get("/",getPatientsInfo)

router.get("/:id",validation(getpatientbyid),getpatientById)

router.patch("/hardExudates/:id",validation(getpatientbyid),postHardEXpic)

router.delete("/:id",validation(getpatientbyid),deletePatient)
router.put("/:id",validation(getpatientbyid),updatePatient)
export default router