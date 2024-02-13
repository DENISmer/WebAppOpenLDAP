import WR_S from "@/components/pages/workroom/workRoom.module.scss"
import React, {useEffect, useRef, useState} from "react";
import {useNavigate} from "react-router";
import {useCookies} from "react-cookie";
import {deleteUser, getUserDataByUid_Admin, getUsersList} from "@/scripts/requests/adminUserProvider";
import loadingGif from "@/assets/icons/h6viz.gif"
import {UserEditForm} from "@/components/pages/workroom/inputItemForEdit";
import {sendChanges} from "@/scripts/requests/adminUserProvider";
import ModalForAddUser from "@/components/Modal_Window/modalForAddUser";


export interface userDataForEdit {
    dn?: string,
    uidNumber?: number,
    gidNumber?: number,
    uid?: string,
    sshPublicKey?: [],
    st?: string[],
    mail?: string[],
    street?: string[],
    cn?: string[],
    displayName?: string,
    givenName?: string[],
    sn?: string[],
    postalCode?: number,
    homeDirectory?: string,
    loginShell?: string,
    objectClass?: string[],
    password?: string
}
export interface SimpleUserDataForEdit {
    sshPublicKey: string[],
    mail: string
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

    const [searchResult1, setSearchResult1] = useState<ListOfUsers[]>(null);
    const [searchValue, setSearchValue] = useState<string>('')

    const navigate = useNavigate();

    const [userAuthCookies, setUserAuthCookie, removeCookie] = useCookies(['userAuth', 'userAttempt'])
    const [currentEditor, setCurrentEditor] = useState<CurrentEditor>()

    let optionRef = useRef<any>(null)
    const [isEditing, setIsEditing] = useState<IeEditing>({isEditing: false, uid: undefined})
    const [userIsChanged, setUserIsChanged] = useState(false)

    const [currentListPage, setCurrentListPage] = useState(1)
    const [pagesCount, setPagesCount] = useState<number>()

    const [userForEditAdmin, setUserForEditAdmin] = useState<userDataForEdit>(null)
    const [editedUser, setEditedUser] = useState<userDataForEdit>(null)
    const [listLoading, setListLoading] = useState<boolean>(false)
    // const [currentUser, setCurrentUser] = useState({})
    const [addUserIsActive, setAddUserIsActive] = useState(false)
    const fillUsersList = async (props: Params) => {
        return await getUsersList(props)
    }

    const getUserData = async (uid: string) => {
        return await getUserDataByUid_Admin(uid, userAuthCookies['userAuth'])
        // console.log(await getUserDataByUid_Admin(uid, userAuthCookies['userAuth']))
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
        } catch { (e) => {
            console.log(e)
        } }
    }, [searchValue,currentListPage])

    //then auth success
    useEffect(() => {
        if (userAuthCookies['userAuth']) {
            if(userAuthCookies['userAuth'].role === 'simple_user') {
                setIsEditing({isEditing: true, uid: userAuthCookies['userAuth'].userName})
            }
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
        console.log(isEditing)
        if(isEditing.isEditing && isEditing.uid){
            getUserData(isEditing.uid)
                .then((response) => {
                    console.log('simple User',response)
                    setUserForEditAdmin(response)
                    setEditedUser(response)
                })
                .catch((e) => {
                    console.log(e)
                })
        } else if (!isEditing.isEditing && isEditing.uid){
            deleteUserFromList()
        }
        // else if (!isEditing.isEditing && isEditing.uid && userAuthCookies.userAuth.role === 'simple_user'){
        //     removeCookie("userAuth")
        //     navigate('/login')
        // }
    }, [isEditing]);

    useEffect(() => {
        console.log(JSON.stringify(editedUser) !== JSON.stringify(userForEditAdmin))
        setUserIsChanged(JSON.stringify(editedUser) !== JSON.stringify(userForEditAdmin))
    },[editedUser])

    const discardChanges = () => {
        if (userIsChanged){
            const isConfirm = confirm("Уверены? Изменения не будут сохранены")
            if (isConfirm && userIsChanged) {
                setIsEditing({isEditing: false, uid: null})
            }
        }
        else setIsEditing({isEditing: false, uid: null})
    }

    const quitForSimpleUser = () => {
        if (userIsChanged) {
            const isConfirm = confirm("Уверены? Изменения не будут сохранены")
            if (isConfirm) {
                removeCookie('userAuth')
                navigate("/login")
            }
        } else {
            removeCookie('userAuth')
            navigate("/login")
        }
    }

    const saveChanges = async ()  => {
        if(!userIsChanged) alert('нет данных для изменения')

        else {
            if(!editedUser.objectClass.includes('ldapPublicKey')){
                delete editedUser['sshPublicKey']
                console.log(editedUser)
            }
            console.log(currentEditor.token)
            await sendChanges(editedUser, currentEditor.token, userAuthCookies.userAuth.role)
                .then((response: any) => {
                    if (response.status === 200){
                        setEditedUser(response.userData)
                        setUserForEditAdmin(response.userData)
                        setUserIsChanged(false)
                        alert("данные сохранены")
                    }
                    else if(response.status === 400) {
                        alert(`ERROR 400 \n ${response.message} \n ${JSON.stringify(response.fields)}`)
                    }
                    else if(response.status === 403) {
                        alert(`ERROR 403 \n ${response.response.data.message}`)
                    }
                })
                .catch((response) => {
                    if (response.status === 400){
                        alert(`ERROR 400 \n ${response.userData}`)
                    }
                    else if (response){
                    }
                })
        }
    }


    // events for event Changes!
    const handleUserDataChange = (newData: userDataForEdit) => {
        setEditedUser(newData);
        // Здесь вы можете также отправить изменения на сервер, если это необходимо.
    };

    // const serDefaultUserData

    const isFieldChanged = (fieldName: keyof userDataForEdit) => {
        const editedUserData = editedUser[fieldName];
        const defaultUserData = userForEditAdmin[fieldName];
        let result;

        let j = 0
        if (Array.isArray(editedUserData) && Array.isArray(defaultUserData)){
            while(j < editedUserData.length){
                if(editedUserData.length !== defaultUserData.length){
                    return true
                }
                result = editedUserData[j] !== defaultUserData[j]
                if(result){
                    return result
                }
                else
                    j++
            }
            return false
        }
        else {
            //setUserIsChanged(editedUser[fieldName] !== userForEditAdmin[fieldName])
            return editedUser[fieldName] !== userForEditAdmin[fieldName];
        }

    };

    const deleteUserFromList = async ()  => {
        const confirmForDelete = confirm(`Вы уверены? \nПользователь ${isEditing.uid} будет удален`)
        if(confirmForDelete){
            await deleteUser(isEditing.uid, currentEditor.token)
                .then((response: any) => {
                    console.log('delete_response',response)
                    if(response.status === 204) {
                        setCurrentListPage(currentListPage + 1)
                        setCurrentListPage(currentListPage - 1)
                        if(currentEditor.uid === isEditing.uid){
                            removeCookie("userAuth")
                            setCurrentEditor(null)
                            navigate("/login")
                        }
                        alert(`Пользователь удален! \n`)
                    }
                })
                .catch((e) => {
                    console.log(e)
                })
        }
    }

    const onCloseModalAddUser = () => {
        const confirmClose = confirm('Уверены?')
        if(confirmClose){
            setAddUserIsActive(false)
        }
    }



    return (<>
        <div className={WR_S.Page}>

            {/*<Modal />*/}
            {addUserIsActive &&
                <ModalForAddUser
                    onClose={onCloseModalAddUser}
                    token={userAuthCookies.userAuth.token ?? currentEditor.token}
                />
            }

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
                            page <button
                            className={listLoading || currentListPage === 1 ? WR_S.Page_Button_disabled : WR_S.Page_Button_Left}
                            onClick={() => pageSwitch(false)}
                            disabled={listLoading || currentListPage === 1}></button>

                            {currentListPage + "..." + pagesCount}

                            <button
                                className={listLoading || currentListPage === pagesCount ? WR_S.Page_Button_disabled_right : WR_S.Page_Button_Right}
                                onClick={() => pageSwitch(true)}
                                disabled={listLoading || currentListPage === pagesCount}></button>
                        </div>

                        {listLoading && <p><img src={loadingGif} alt="loading.."/></p>}

                        <div className={WR_S.SearchList}>
                            <button onClick={() => setAddUserIsActive(true)}>add user</button>
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
                                        <button className={WR_S.Edit_Button}
                                                onClick={() => setIsEditing({isEditing: true, uid: element.uid})}>edit
                                        </button>
                                        <button className={WR_S.Delete_Button} onClick={() => setIsEditing({
                                            isEditing: false,
                                            uid: element.uid
                                        })}>delete
                                        </button>
                                    </div>
                                </div>)
                            )}
                        </div>
                    </div>
                </div>}

            {currentEditor && isEditing && isEditing.isEditing && editedUser && <div className={WR_S.Admin_UseProfile}>
                {userIsChanged && <div>Есть изменения</div>}
                <UserEditForm userData={editedUser} onUserDataChange={handleUserDataChange} fieldIsChange={isFieldChanged} role={userAuthCookies['userAuth'].role}/>

            </div>}

            {currentEditor && isEditing && isEditing.isEditing && editedUser && <div className={WR_S.button_group}>
                <button className={WR_S.submitButton} onClick={() => saveChanges()}>сохранить изменения
                </button>
                <button className={WR_S.cancelChanges}
                        onClick={() => {
                            userAuthCookies.userAuth.role === 'simple_user' ?
                                quitForSimpleUser() : discardChanges()
                        }}>выйти к {currentEditor.role === 'webadmins' ? <span>списку</span> : <span>авторизации</span>}
                </button>
            </div>}

            {/*{currentEditor && currentEditor.role !== 'webadmins' && editedUser &&*/}
            {/*    <div className={WR_S.Admin_Panel}>*/}
            {/*        <div className={WR_S.Admin_UseProfile}>*/}
            {/*            /!*{JSON.stringify(editedUser)}*!/*/}
            {/*            <UserEditForm userData={editedUser} onUserDataChange={handleUserDataChange} fieldIsChange={isFieldChanged} role={userAuthCookies['userAuth'].role}/>*/}

            {/*            {currentEditor && currentEditor.role === 'simple_user' && isEditing && isEditing.isEditing && editedUser && <div className={WR_S.button_group}>*/}
            {/*                <button className={WR_S.submitButton} onClick={() => saveChanges()}>сохранить изменения*/}
            {/*                </button>*/}
            {/*                <button className={WR_S.cancelChanges}*/}
            {/*                        onClick={() => {*/}
            {/*                            discardChanges()*/}
            {/*                        }}>выйти к списку*/}
            {/*                </button>*/}
            {/*            </div>}*/}
            {/*        </div>*/}
            {/*    </div>*/}
            {/*}*/}
        </div>
    </>)
}

export default WorkRoom;
