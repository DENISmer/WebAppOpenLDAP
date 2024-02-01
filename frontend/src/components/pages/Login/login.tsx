import L_S from '@/components/pages/Login/login.module.scss';
import openEye from "@/assets/icons/openEyePass.png"
import closeEye from "@/assets/icons/closedEyePass.png"
import {useEffect, useState} from "react";
import {useNavigate} from "react-router";
import setAuthToken, {AuthParams, UserAuth} from "@/scripts/requests/auth";
import {useCookies} from "react-cookie";
const Login = () => {

    const [showPass,setShowPass] = useState(true)
    const [password, setPassword] = useState<string>(null)
    const [username, setUsername] = useState<string>(null)
    const [cookies, setCookie, removeCookie] = useCookies(['userAuth'])
    //const navigate = useNavigate();

    useEffect(() => {
      console.log(cookies['userAuth'])
    },[])
    const sendParams = async (user: string, pass: string) => {
        if(user && pass){
            const params: AuthParams = {
                userName: user,
                password: pass
            }
            return await setAuthToken(params)
        } else {
            console.log('error')
        }
    }

    const setCurrentUserCookie = async () => {
        try {
            const userData: UserAuth | undefined = await sendParams(username, password)
            console.log('UserData: ',userData)
                setCookie('userAuth', userData, {maxAge: 300})
        } catch (e){
            console.log(e.message,'Auth failed')
        }
    }

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
                    <input
                        className={L_S.inputUsername}
                        type="text"
                        placeholder={"username"}
                        value={username}
                        onChange={(event) => setUsername(event.target.value)}
                    />
                    <div className={L_S.passField}>
                        <input
                            className={L_S.inputPass}
                            type={showPass ? "password" : "text"}
                            placeholder={"password"}
                            value={password}
                            onChange={(event) => setPassword(event.target.value)}
                        />
                        <img className={L_S.passSwitch} onClick={() => passVisibility()} src={showPass ? openEye : closeEye} width={19} alt={"show"}/>
                    </div>
                </div>
                <input className={L_S.submitButton} type="submit" value={"login"} onClick={() => setCurrentUserCookie()}/>
            </form>
        </div>
    </div>
    </>)
}

export default Login;
