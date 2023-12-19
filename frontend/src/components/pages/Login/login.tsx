import L_S from '@/components/pages/Login/login.module.scss';
import openEye from "@/assets/icons/openEyePass.png"
import closeEye from "@/assets/icons/closedEyePass.png"
import {useState} from "react";
import {useNavigate} from "react-router";
const Login: React.FC = () => {

    const [showPass,setShowPass] = useState(true)
    const navigate = useNavigate();
    const passVisibility = () => {
        setShowPass(!showPass);
    }
    return (<>
    <div className={L_S.Page}>
        <div className={L_S.Content}>
            <div className={L_S.Title}>
                Welcome to the OpenLPAD web service
            </div>
            <form className={L_S.LoginForm} action="#">
                <div className={L_S.inputsField}>
                    <input className={L_S.inputUsername} type="text" placeholder={"username"}/>
                    <div className={L_S.passField}>
                        <input className={L_S.inputPass} type={showPass ? "password" : "text"} placeholder={"password"}/>
                        <img className={L_S.passSwitch} onClick={() => passVisibility()} src={showPass ? openEye : closeEye} width={19} alt={"show"}/>
                    </div>
                </div>
                <input className={L_S.submitButton} type="submit" value={"login"} onClick={() => navigate("/")}/>
            </form>
        </div>
    </div>
    </>)
}

export default Login;
