import WR_S from "@/components/pages/workroom/workRoom.module.scss"
// import React from "react";
import {test} from "@/assets/testList";
import {useState} from "react";

const WorkRoom: React.FC = () => {

    const [subject,setSubject] = useState(null)

    return (<>
        <div className={WR_S.Page}>
            <div className={WR_S.Admin_listOfUsers}>
                <div className={WR_S.menu}>
                    <div className={WR_S.logout}>⬅</div>
                    <div className={WR_S.Admin_Profile}></div>
                </div>
                <input list={"browsers"} type={"text"} className={WR_S.Admin_listOfUsers}
                       placeholder={'Введите имя'}
                       value={subject}
                       onChange={(e) => {
                           setSubject(e.target.value)
                           // setReadyToTheNextPage(false)
                       }}/>
                <datalist id="browsers">
                    {test.map((element,index)=>(<option key={index} value={element.tag}>{element.name}</option>)
                    )}
                </datalist>
            </div>
            <div className={WR_S.Admin_UseProfile}>

            </div>
        </div>
    </>)
}

export default WorkRoom;
