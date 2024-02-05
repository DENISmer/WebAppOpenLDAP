import WR_S from "@/components/pages/workroom/workRoom.module.scss"
import {test} from "@/assets/users_from_ldap";
import {useEffect, useRef, useState} from "react";
import {useNavigate} from "react-router";
import settingFieldsToChange from "@/scripts/workroom/settingFieldsToChange";
import {useCookies} from "react-cookie";
import { getUserDataByUid_Admin, getUsersList} from "@/scripts/requests/adminUserProvider";

export interface userDataForEdit {
    dn: string,
    uidNumber: number,
    gidNumber: number,
    uid: string,
    sshPublicKey: [],
    st: string[],
    mail: string[],
    street: string[],
    cn: string[],
    displayName: string,
    givenName: string[],
    sn: string[],
    postalCode: number[],
    homeDirectory: string,
    loginShell: string,
    objectClass: string[]
}
interface CurrentEditor {
    token: string,
    role: string,
    uid: string,
}
interface CurrentSearchResponse {
    items: [],
    num_items: number,
    num_pages: number,
    page: number
}

export interface ListOfUsers {
    dn: string
    uid: string
    cn: string
    sn: string
    gidNumber: string
    uidNumber: string
}
export interface Params {
    value: string,
    pageNumber: number,
    token: string
}

export interface IeEditing {
    isEditing: boolean,
    uid: string
}
const WorkRoom: React.FC = () => {

    const [subject,setSubject] = useState();
    const [searchResult1, setSearchResult1] = useState<ListOfUsers[]>(null);
    const [searchResult, setSearchResult] = useState<any[]>(null);
    const navigate = useNavigate();
    const [viewFields, setViewFields] = useState<any[]>()
    const [userAuthCookies, setUserAuthCookie, removeCookie] = useCookies(['userAuth', 'userAttempt'])
    const [currentEditor, setCurrentEditor] = useState<CurrentEditor>()
    const [searchValue, setSearchValue] = useState<string>('')
    let optionRef = useRef<any>(null)
    const [isEditing, setIsEditing] = useState<IeEditing>({isEditing: false, uid: undefined})
    const [currentListPage, setCurrentListPage] = useState(1)
    const [pagesCount, setPagesCount] = useState<number>()
    const [userForEditAdmin, setUserForEditAdmin] = useState<userDataForEdit>(null)
    const [editedUser, setEditedUser] = useState<userDataForEdit>(null)
    // const [currentUser, setCurrentUser] = useState({})
    const fillUsersList = async (props: Params) => {
        return await getUsersList(props)
    }

    const getUserData = async (uid: string) => {
        return await getUserDataByUid_Admin(uid)
    }

    const pageSwitch = (next: boolean) => {
        next ? currentListPage < pagesCount && setCurrentListPage(currentListPage + 1) :
            currentListPage > 1 && setCurrentListPage(currentListPage - 1)
    }

    useEffect(() => {
        try{
            fillUsersList({value : searchValue,pageNumber: currentListPage,token : userAuthCookies['userAuth'].token})
                .then((response) => {
                    if (response && response.status && response.status === 200) {
                        response.data.items && setSearchResult1(response.data.items)
                        response.data.page && setCurrentListPage(response.data.page)
                        response.data.num_pages && setPagesCount(response.data.num_pages)
                    }
                    else {
                        console.log(response)
                    }
                })
        } catch { (e: any) => {
            console.log(e)
        } }
    }, [searchValue,currentListPage])

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

    useEffect(() => {
        if(isEditing.isEditing && isEditing.uid){
            getUserData(isEditing.uid)
                .then((response) => {
                    console.log(response)
                    setUserForEditAdmin(response)
                    setEditedUser(response)
                })
                .catch((e) => {
                    console.log(e)
                })
        }
    }, [isEditing]);


    // events for event Changes!
    const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        const { name, value } = event.target;
        setEditedUser({ ...editedUser, [name]: value });
    };

    const isFieldChanged = (fieldName: keyof userDataForEdit) => {
        console.log(editedUser[fieldName], userForEditAdmin[fieldName])
        return editedUser[fieldName] !== userForEditAdmin[fieldName];
    };

    const testMethod = () => {
        searchResult ? setViewFields(settingFieldsToChange(searchResult[0]).publicMethod()) : null
    }

    return (<>
        <div className={WR_S.Page}>
            <div className={WR_S.menu}>
                <div className={WR_S.logout} onClick={() => {
                    removeCookie('userAuth')
                    navigate('/login')
                }}>выйти
                </div>
                <div className={WR_S.Admin_Profile}>профиль</div>
            </div>

            {currentEditor && currentEditor.role === 'webadmins' &&
                isEditing && !isEditing.isEditing && <div className={WR_S.Admin_Panel}>
                {/*menu*/}

                {/*seacrh and list of users*/}
                <div>
                        <input list={"browsers"} type={"text"} className={WR_S.select}
                               placeholder={'Введите имя'}
                               value={searchValue}
                               onChange={(e) => {
                                   setSearchValue(e.target.value)
                               }}
                        />

                        <div className={WR_S.pageSelect}>
                            page <div onClick={() => pageSwitch(false)}>{`<`}</div>
                            {currentListPage}
                            <div onClick={() => pageSwitch(true)}>{`>`}</div>
                        </div>

                        <div className={WR_S.SearchList}>
                            {searchResult1 && searchResult1.map((element, index) => (
                                <div className={WR_S.UsersListItem}
                                     key={index}
                                     ref={optionRef}
                                >
                                    {element.cn + " | " + element.sn + " | " + element.uid
                                        + " | " + element.gidNumber}
                                    <button onClick={() => setIsEditing({isEditing: true, uid: element.uid})}>edit
                                    </button>
                                </div>)
                            )}
                        </div>

                    </div>
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
            </div>}

            {isEditing && isEditing.isEditing && editedUser && <div className={WR_S.Admin_UseProfile}>
                {Object.keys(editedUser).map((obj, indexOfAll) => (
                    <div style={{maxWidth: "24%"}}>
                        {/*NO DAVE*/}
                        {editedUser[obj] && typeof editedUser[obj] !== "object" &&
                        <div className={WR_S.field}>
                            <div>{[obj]}</div>
                            <input type={typeof editedUser[obj] === "number" ? "number" : "text"}
                                   name={obj}
                                   value={(editedUser as any)[obj]}
                                   onChange={handleInputChange}
                                   className={isFieldChanged(obj as keyof userDataForEdit) ? WR_S.input_changed : null}
                            />
                            {/*{isFieldChanged(obj as keyof userDataForEdit) ? <span>Изменено</span> : null}*/}
                        </div>}

                        {/* for object*/}
                        {typeof userForEditAdmin[obj] === 'object' && userForEditAdmin[obj] !== null && userForEditAdmin[obj].length > 1 &&
                            userForEditAdmin[obj].map((item, index) =>(
                                <div className={WR_S.field}>
                                    {[index]}
                                    <input type="text" value={item}/>
                                </div>)
                            )
                        }
                    </div>
                ))}
                <button className={WR_S.submitButton} onClick={() => console.log(editedUser)}>сохранить изменения
                </button>
                <button className={WR_S.cancelChanges}
                        onClick={() => setIsEditing({isEditing: false, uid: null})}>отменить изменения
                </button>
            </div>}
        </div>
    </>)
}

export default WorkRoom;
