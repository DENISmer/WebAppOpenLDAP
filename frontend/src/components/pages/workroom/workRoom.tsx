import WR_S from "@/components/pages/workroom/workRoom.module.scss"
// import React from "react";
import {test} from "@/assets/testList";
import {useEffect, useState} from "react";
import {useNavigate} from "react-router";

const WorkRoom: React.FC = () => {

    const [subject,setSubject] = useState(null);
    const navigate = useNavigate();
    // const [currentUser, setCurrentUser] = useState({})

    useEffect(() => {
        console.log(subject)
        console.log(test[subject])
    }, [subject])

    return (<>
        <div className={WR_S.Page}>
            <div className={WR_S.Admin_listOfUsers}>
                <div className={WR_S.menu}>
                    <div className={WR_S.logout} onClick={() => navigate('/login')}>выйти</div>
                    <div className={WR_S.Admin_Profile}>профиль</div>
                </div>
                <input list={"browsers"} type={"text"} className={WR_S.select}
                       placeholder={'Введите имя'}
                       value={subject}
                       onChange={(e) => {
                           setSubject(e.target.value)
                       }}
                />
                <datalist id="browsers">
                    {test.map((element,index)=>(
                        <option key={index} value={element.id} >
                            {element.name}
                        </option>)
                    )}
                </datalist>
                { subject && test[subject] ? <div className={WR_S.AdminCurrentUser}>
                    <div className={WR_S.CurrentUserName}>
                        {test[subject].name}
                    </div>
                    <div className={WR_S.CurrentUserUid}>
                        {test[subject].id}<br/>
                        {test[subject].info}
                    </div>
                </div> : null}
            </div>

            <div className={WR_S.Admin_UseProfile}>

            </div>
        </div>
    </>)
}

export default WorkRoom;
