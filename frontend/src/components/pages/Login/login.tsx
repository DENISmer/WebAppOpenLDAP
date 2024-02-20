import L_S from '@/components/pages/Login/login.module.scss';
import openEye from "@/assets/icons/openEyePass.png"
import closeEye from "@/assets/icons/closedEyePass.png"
import {useEffect, useState} from "react";
import {useNavigate} from "react-router";
import setAuthToken, {AuthParams, UserAuth} from "@/scripts/requests/auth";
import {useCookies} from "react-cookie";
import loadingGif from "@/assets/icons/h6viz.gif";
const Login = () => {

    const [showPass,setShowPass] = useState(true)
    const [password, setPassword] = useState<string>(null)
    const [username, setUsername] = useState<string>(null)
    const [userAuthCookies, setUserAuthCookie, removeCookie] = useCookies(['userAuth', 'userAttempt'])
    const navigate = useNavigate();
    const [authError, setAuthError] = useState(false)
    const [attemptCounter, setAttemptCounter] = useState(7)
    const [loading, setLoading] = useState(false)

    useEffect(() => {
        //setUserAuthCookie('userAuth', undefined)
        console.log(userAuthCookies['userAuth'])
    },[])

    useEffect(() => {
        if (attemptCounter < 1){
            setUserAuthCookie('userAttempt', false, {maxAge: 10})
        }
    }, [attemptCounter]);

    useEffect(() => {
        !userAuthCookies['userAttempt'] && setAttemptCounter(7)
    }, [userAuthCookies['userAttempt']]);

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

    const setCurrentUserCookie = async (e) => {
        e.preventDefault()
        if(attemptCounter > 0){
            if(password && username && (password.length >= 3 && username.length >= 2)){
                try {
                    setLoading(true)
                    const userData: UserAuth | undefined = await sendParams(username, password)
                    if(userData.status === 200){
                        setUserAuthCookie('userAuth', userData, {maxAge: 3600 * 6})
                        setAuthError(false)
                        setLoading(false)
                        navigate("/")
                    }
                    else {
                        setAttemptCounter(attemptCounter - 1)
                        setAuthError(true)
                        setLoading(false)
                    }
                } catch (e){
                    setAuthError(true)
                    setLoading(false)
                    console.log(e.message,'Auth failed')
                }
            } else {
                setAuthError(true)
                setLoading(false)
            }
        } else {
            setUserAuthCookie('userAttempt', false, {maxAge: 120})
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
            <form className={L_S.LoginForm} onSubmit={setCurrentUserCookie}>
                {authError ?
                    <div style={{color: "red", fontSize: "18px"}}>Проверьте введенные данные</div> :
                    null}
                <div className={L_S.inputsField}>
                    <input
                        id={'username'}
                        className={authError ? L_S.inputUsername_error + ' ' + L_S.inputUsername : L_S.inputUsername}
                        type="text"
                        placeholder={"username"}
                        value={username}
                        onChange={(event) => {
                            setUsername(event.target.value)
                            setAuthError(false)
                        }}
                    />
                    <div className={L_S.passField}>
                        <input
                            className={authError ? L_S.inputPass + ' ' + L_S.inputUsername_error : L_S.inputPass}
                            type={showPass ? "password" : "text"}
                            placeholder={"password"}
                            value={password}
                            onChange={(event) => {
                                setPassword(event.target.value)
                                setAuthError(false)
                            }}
                        />
                        <img className={L_S.passSwitch} onClick={() => passVisibility()} src={showPass ? openEye : closeEye} width={24} alt={"show"}/>
                    </div>
                </div>
                <input className={L_S.submitButton}
                        disabled={authError || (userAuthCookies['userAttempt'] !== undefined && !userAuthCookies['userAttempt'])}
                        id={"submit"}
                        value={"Login"}
                        type={"submit"}
                />{loading && <img src={loadingGif} alt={"loading.."}/>}
                {userAuthCookies['userAttempt'] !== undefined && !userAuthCookies['userAttempt'] && <p style={{color: 'red', marginBottom: '10px'}}>Слишком много попыток. Перезайгрузите страницу и попробуйте позже</p>}
                </form>

        </div>
    </div>
    </>)
}

export default Login;
