import WR_S from "@/components/pages/workroom/workRoom.module.scss"
import React, {useEffect, useRef, useState} from "react";
import {useNavigate} from "react-router";
import settingFieldsToChange from "@/scripts/workroom/settingFieldsToChange";
import {useCookies} from "react-cookie";
import { getUserDataByUid_Admin, getUsersList} from "@/scripts/requests/adminUserProvider";
import loadingGif from "@/assets/icons/h6viz.gif"
import {UserEditForm} from "@/components/pages/workroom/inputItemForEdit";
import {sendChanges} from "@/scripts/requests/adminUserProvider";
import Modal from "@/components/Modal_Window/modalWindow";
import IntrinsicAttributes = React.JSX.IntrinsicAttributes;

export interface userDataForEdit {
    dn: string,
    uidNumber?: number,
    gidNumber?: number,
    uid: string,
    sshPublicKey?: [],
    st?: string[],
    mail?: string[],
    street?: string[],
    cn: string[],
    displayName?: string,
    givenName?: string[],
    sn: string[],
    postalCode?: number,
    homeDirectory: string,
    loginShell?: string,
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
    const [searchValue, setSearchValue] = useState<string>('')

    const navigate = useNavigate();

    const [userAuthCookies, setUserAuthCookie, removeCookie] = useCookies(['userAuth', 'userAttempt'])
    const [currentEditor, setCurrentEditor] = useState<CurrentEditor>()

    let optionRef = useRef<any>(null)
    const [isEditing, setIsEditing] = useState<IeEditing>({isEditing: false, uid: undefined})

    const [currentListPage, setCurrentListPage] = useState(1)
    const [pagesCount, setPagesCount] = useState<number>()

    const [userForEditAdmin, setUserForEditAdmin] = useState<userDataForEdit>(null)
    const [editedUser, setEditedUser] = useState<userDataForEdit>(null)
    const [listLoading, setListLoading] = useState<boolean>(false)
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
        setListLoading(true)
        try{
            fillUsersList({value : searchValue,pageNumber: currentListPage,token : userAuthCookies['userAuth'].token})
                .then((response) => {
                    if (response && response.status && response.status === 200) {
                        response.data.items && setSearchResult1(response.data.items)
                        response.data.page && setCurrentListPage(response.data.page)
                        response.data.num_pages && setPagesCount(response.data.num_pages)
                        setListLoading(false)
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

    const handleUserDataChange = (newData: userDataForEdit) => {
        setEditedUser(newData);
        // Здесь вы можете также отправить изменения на сервер, если это необходимо.
    };

    const isFieldChanged = (fieldName: keyof userDataForEdit) => {
        return editedUser[fieldName] != userForEditAdmin[fieldName];
    };

    const saveChanges = () => {

    }

    // const testMethod = () => {
    //     searchResult ? setViewFields(settingFieldsToChange(searchResult[0]).publicMethod()) : null
    // }


    return (<>
        <div className={WR_S.Page}>

            <Modal />

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
                <div className={WR_S.Information_Window}>
                        <input list={"browsers"} type={"text"} className={WR_S.Input} required
                               // placeholder={'Введите имя'}
                               value={searchValue}
                               onChange={(e) => {
                                   setSearchValue(e.target.value)
                               }}
                        />
                        <span className={WR_S.bar}></span>
                        <label className={WR_S.Label}>Введите имя</label>

                        <div className={WR_S.pageSelect}>
                            page <button className={WR_S.Page_Button_Left} onClick={() => pageSwitch(false)}
                                         disabled={listLoading || currentListPage === 1}></button>

                            {currentListPage}

                            <button className={WR_S.Page_Button_Right} onClick={() => pageSwitch(true)}
                                    disabled={listLoading || currentListPage === pagesCount}></button>
                        </div>
                        {listLoading && <p><img src={loadingGif} alt="loading.."/></p>}

                        <div className={WR_S.SearchList}>
                            {!listLoading && searchResult1 && searchResult1.map((element, index) => (
                                <div className={WR_S.UsersListItem}
                                     key={index}
                                     ref={optionRef}
                                >
                                    <div className={WR_S.Div_User_List}>
                                        <ol className={WR_S.User_List}>
                                            <li data-list='Gid Number'> &nbsp;{element.gidNumber}</li>
                                            <li data-list=' | Coomon Name'>&nbsp;{element.cn}</li>
                                            <li data-list=' | Surname'> &nbsp;{element.sn}</li>
                                            <li data-list='| User ID'> &nbsp;{element.uid}</li>
                                        </ol>
                                        {/*{element.cn + " | " + element.sn + " | " + element.uid*/}
                                        {/*    + " | " + element.gidNumber}*/}
                                    </div>
                                    <div className={WR_S.Button_Group}>
                                        <button className={WR_S.Edit_Button} onClick={() => setIsEditing({isEditing: true, uid: element.uid})}>edit
                                        </button>
                                        <button className={WR_S.Delete_Button} onClick={() => setIsEditing({isEditing: true, uid: element.uid})}>delete</button>
                                    </div>
                                </div>)
                            )}
                        </div>
                    </div>
            </div>}

            {isEditing && isEditing.isEditing && editedUser && <div className={WR_S.Admin_UseProfile}>
                <UserEditForm userData={editedUser} onUserDataChange={handleUserDataChange} />

                <button className={WR_S.submitButton} onClick={() => sendChanges(editedUser)}>сохранить изменения
                </button>
                <button className={WR_S.cancelChanges}
                        onClick={() => setIsEditing({isEditing: false, uid: null})}>отменить изменения
                </button>
            </div>}
        </div>
    </>)
}

export default WorkRoom;
