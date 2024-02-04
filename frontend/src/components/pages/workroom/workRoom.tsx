import WR_S from "@/components/pages/workroom/workRoom.module.scss"
// import React from "react";
import {test} from "@/assets/users_from_ldap";
import {useEffect, useState} from "react";
import {useNavigate} from "react-router";
import settingFieldsToChange from "@/scripts/workroom/settingFieldsToChange";
import {useCookies} from "react-cookie";
import {getUsersList} from "@/scripts/requests/adminUserProvider";

interface CurrentEditor {
    token: string,
    role: string,
    uid: string,
}

export interface ListOfUsers {
    dn?: string
    uid?: string
    cn?: string
    sn?: string
    gidNumber: string
    uidNumber: string
}
export interface Params {
    value: string,
    token: string
}
const WorkRoom: React.FC = () => {

    const [subject,setSubject] = useState();
    const [searchResult, setSearchResult] = useState(null);
    const navigate = useNavigate();
    const [viewFields, setViewFields] = useState<any[]>()
    const [userAuthCookies, setUserAuthCookie, removeCookie] = useCookies(['userAuth', 'userAttempt'])
    const [currentEditor, setCurrentEditor] = useState<CurrentEditor>()
    const [searchValue, setSearchValue] = useState<string>()
    // const [currentUser, setCurrentUser] = useState({})

    const fillUsersList = async (props: Params) => {
        // const resultSearchList : ListOfUsers | undefined = await getUsersList(props)
        // return resultSearchList
        return await getUsersList(props)
    }

    useEffect(() => {
        fillUsersList({value : searchValue,token : userAuthCookies['userAuth'].token})
    }, [searchValue])

    useEffect(() => {
        if (userAuthCookies['userAuth']) {
            setCurrentEditor({
                    token: userAuthCookies['userAuth'].token,
                    role: userAuthCookies['userAuth'].role,
                    uid: userAuthCookies['userAuth'].userName,
                }
            )
        } else {
            navigate("/login")
        }
        console.log(userAuthCookies['userAuth'])
    }, []);

    const testMethod = () => {
        searchResult ? setViewFields(settingFieldsToChange(searchResult[0]).publicMethod()) : null
    }

    return (<>
        <div className={WR_S.Page}>
            <div className={WR_S.Admin_listOfUsers}>
                <div className={WR_S.menu}>
                    <div className={WR_S.logout} onClick={() => {
                        removeCookie('userAuth')
                        navigate('/login')
                    }}>выйти</div>
                    <div className={WR_S.Admin_Profile}>профиль</div>
                </div>
                {currentEditor && currentEditor.role === 'webadmins' && <div>
                    <input list={"browsers"} type={"text"} className={WR_S.select}
                           placeholder={'Введите имя'}
                           value={searchValue}
                           onChange={(e) => {
                               setSearchValue(e.target.value)
                           }}
                    />
                    <datalist id="browsers">
                        {test.map((element, index) => (
                            <option key={index} value={element.uidNumber}>
                                {element.displayName + " | " + element.street + " | " + element.mail
                                    + " | " + element.givenName}
                            </option>)
                        )}
                    </datalist>
                </div>}
                {/*showing current user information*/}
                {subject && searchResult[0] ? <div className={WR_S.AdminCurrentUser}>
                    {/*takes current user object*/}
                    {Object.keys(searchResult).map((obj, index) => (
                        <div key={index} className={WR_S.CurrentUserName}>
                            Name: {searchResult[obj].displayName}
                            <br/>
                            uid: {searchResult[obj].uid}
                            <div className={WR_S.CurrentUserUid}>
                                uidNumber: {searchResult[0].uidNumber}<br/>
                                {/*mail render*/}
                                mail: {typeof searchResult[0].mail === 'object' ? searchResult[0].mail.map((mail, index) => (
                                <div key={index}>
                                    {index + 1 + ". " + mail}
                                </div>
                            )) : <div>{searchResult[0].mail}</div>}
                            </div>
                        </div>
                    ))}
                    <button onClick={() => testMethod()}>подтвердить выбор</button>
                </div> : null}
            </div>

            <div className={WR_S.Admin_UseProfile}>
                {viewFields && Object.keys(viewFields).map((obj, indexOfAll) => (
                    <div> {[obj]}
                        {typeof viewFields[obj] === "object" && viewFields[obj].length > 0 ?
                            viewFields[obj].map((field, index) => (
                                field.length > 20 ?
                                <div className={WR_S.field}>{indexOfAll + '.' + (index + 1)}
                                    <textarea value={field} key={index} cols={10} rows={2}></textarea>
                                </div>
                                :
                                    <div className={WR_S.field}>{indexOfAll + '.' + (index + 1)}
                                        <input value={field} key={index}/>
                                    </div>
                            ))
                            :
                            <div className={WR_S.field}>{indexOfAll + 1}
                                <input value={viewFields[obj]} key={indexOfAll}/>
                            </div>}
                    </div>
                    ))}
                <button className={WR_S.submitButton} onClick={() => console.log(currentEditor)}>сохранить изменения</button>
                <button className={WR_S.cancelChanges}>отменить изменения</button>
            </div>
        </div>
    </>)
}

export default WorkRoom;
