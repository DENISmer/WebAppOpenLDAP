import WR_S from "@/components/pages/workroom/workRoom.module.scss"
import React, {useEffect, useRef, useState} from "react";
import {useNavigate} from "react-router";
import {useCookies} from "react-cookie";
import {
    deleteUser,
    ErrorData,
    getUserDataByUid_Admin,
    getUserGroupData,
    getUsersList
} from "@/scripts/requests/adminUserProvider";
import loadingGif from "@/assets/icons/h6viz.gif"
import {UserEditForm} from "@/components/pages/workroom/editor/userEditor/inputItemForEdit";
import {sendChanges} from "@/scripts/requests/adminUserProvider";
import ModalForAddUser from "@/components/Modal_Window/modalForAddUser";
import pen from "@/assets/icons/pen_edit1.png"
import delete_user from "@/assets/icons/delete_user.png"
import {ProfileView} from "@/components/pages/workroom/editor/ProfileView/ProfileView";
import {UserGroupForm} from "@/components/pages/workroom/editor/userGroupEditor/userGroupForm";
import {response} from "express";


export interface userDataForEdit {
    jpegPhoto? : string,
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
    userPassword?: string,
    error?: any
}
export interface userGroupDataForEdit {
    dn: string,
    gidNumber: number,
    cn: string,
    objectClass: string[],
    memberUid: string,
    status?: number,
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

export interface IsEditing {
    isEditing: boolean,
    uid: string
}
export interface UserRole {
    admin: string,
    simple: string,
}
const WorkRoom: React.FC = () => {

    const [searchResult1, setSearchResult1] = useState<ListOfUsers[]>(null);
    const [searchValue, setSearchValue] = useState<string>('')

    const navigate = useNavigate();

    const [userAuthCookies, setUserAuthCookie, removeCookie] = useCookies(['userAuth', 'userAttempt'])
    const [currentEditor, setCurrentEditor] = useState<CurrentEditor>()

    let optionRef = useRef<any>(null)
    const [isEditing, setIsEditing] = useState<IsEditing>({isEditing: false, uid: undefined})
    const [isEditingGroup, setIsEditingGroup] =useState(false)
    const [userIsChanged, setUserIsChanged] = useState(false)

    const [currentListPage, setCurrentListPage] = useState(1)
    const [pagesCount, setPagesCount] = useState<number>()

    const [userForEditAdmin, setUserForEditAdmin] = useState<userDataForEdit>(null)
    const [editedUser, setEditedUser] = useState<userDataForEdit>(null)
    const [listLoading, setListLoading] = useState<boolean>(false)

    const [adminUserEdit, setAdminUserEdit] = useState(false)
    // const [currentUser, setCurrentUser] = useState({})
    const [addUserIsActive, setAddUserIsActive] = useState(false)

    const role: UserRole = {
        admin: 'webadmin',
        simple: 'simple_user',
    }

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
        onUserListPageChange()
    }, [currentListPage])

    useEffect(() => {
        setCurrentListPage(1);
        onUserListPageChange()
    },[searchValue])

    //then auth success
    useEffect(() => {
        if (userAuthCookies['userAuth']) {
            if(userAuthCookies['userAuth'].role === role.simple) {
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


    // hook works after editing trigger
    useEffect(() => {
        console.log(isEditing)
        if(isEditing.isEditing && isEditing.uid){
            getUserData(isEditing.uid)
                .then((response: userDataForEdit ) => {
                    if (response.error && response.error.status === 401){
                        removeCookie('userAuth');
                        navigate('/login')
                    }
                    setUserForEditAdmin(response)
                    setEditedUser(response)
                })
                .catch((e) => {
                    console.log("error catched",e)
                })
        } else if (!isEditing.isEditing && isEditing.uid){
            deleteUserFromList()
        }
    }, [isEditing]);

    //hooks for switch to the user group edit mode
    useEffect( () => {
        isEditingGroup && groups()
            .then((response): userGroupDataForEdit | ErrorData => {
                if(response.status){
                       alert(`ERROR ${response.status}`)
                } else {
                    alert('Good')
                }
                return null
            })
    },[isEditingGroup])


    useEffect(() => {
        console.log(JSON.stringify(editedUser) !== JSON.stringify(userForEditAdmin))
        setUserIsChanged(JSON.stringify(editedUser) !== JSON.stringify(userForEditAdmin))
    },[editedUser])


    const onUserListPageChange = () => {
        setListLoading(true)
        try{
            fillUsersList({value : searchValue,pageNumber: currentListPage,token : userAuthCookies['userAuth'].token})
                .then((response) => {
                    if (response && response.status && response.status === 200) {
                        response.data.items && setSearchResult1(response.data.items)
                        //response.data.page && setCurrentListPage(response.data.page)
                        response.data.num_pages && setPagesCount(response.data.num_pages)
                        setListLoading(false)
                    }
                    else {
                        if(response && response.response.status === 401){
                            removeCookie('userAuth')
                            navigate('/login')
                        }
                    }
                })
                .catch((e) => {
                    console.log(e)
                })
        } catch { (e) => {
            console.log(e)
        } }
    }

    const groups = async () : Promise<userGroupDataForEdit | ErrorData> => {
        return await getUserGroupData(
            {token: currentEditor.token,
                uid: editedUser.uid
            })
    }

    const quitForAdmin = () => {
        if (userIsChanged){
            const isConfirm = confirm("Уверены? Изменения не будут сохранены")
            if (isConfirm && userIsChanged) {
                setIsEditing({isEditing: false, uid: null})
            }
        }
        else setIsEditing({isEditing: false, uid: null})
    }


    const discardChanges = () => {
        if(userIsChanged){
            const askForDiscard = confirm("Все изменения будут сброшены. Продолжить?")
            askForDiscard ? setEditedUser(userForEditAdmin) : null
        } else {
            alert("Изменений нет")
        }

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
            await sendChanges(editedUser, currentEditor.token,currentEditor.role ?? userAuthCookies.userAuth.role)
                .then((response: any) => {
                    if (response.status === 200){
                        setEditedUser(response.userData)
                        setUserForEditAdmin(response.userData)
                        setUserIsChanged(false)
                        alert("данные сохранены")
                    }
                    else if(response.status === 401) {
                        alert(`ERROR 401 \n ${response.message}`)
                        removeCookie('userAuth')
                        navigate('/login')
                    }
                    else if(response.status === 403) {
                        alert(`ERROR 403 \n ${response.message}`)
                    }
                    else if (response.status === 400){
                        alert(`ERROR 400 \n ${response.message}\n${JSON.stringify(response.fields)}`)
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
        // Здесь вы можете отправить изменения на сервер, если это необходимо.
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
    const unLogin = () => {
        if(userIsChanged){
            const askForUnLogin = confirm("Есть не сохраненные изменения. Все равно выйти?")
            if (askForUnLogin) {
                removeCookie('userAuth')
                navigate('/login');
            }
        } else {
            removeCookie('userAuth')
            navigate('/login');
        }
    }

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

    const setCurrentAdminProfileEdit = () => {
        if(isEditing.isEditing){
            const askForClose = confirm('Текущие изменения не сохранятся. Продолжить?')
            if (askForClose){
                setIsEditing(
                    {
                        isEditing: true,
                        uid: currentEditor.uid
                    }
                )
                setAdminUserEdit(true)
            }
        } else {
            setIsEditing(
                {
                    isEditing: true,
                    uid: currentEditor.uid
                }
            )
        }
    }

    const onCloseModalAddUser = (data: boolean) => {
        if(data){
            setAddUserIsActive(false)
        }
        else {
            const confirmClose = confirm('Введенные данные не сохранятся. Продолжить?')
            if(confirmClose){
                setAddUserIsActive(false)
            }
        }
    }


    const switchEditMode = () => {
        setIsEditingGroup(!isEditingGroup)
    }

    return (<>
        <div className={WR_S.Page}>

            {/*<Modal />*/}
            {addUserIsActive && userAuthCookies && userAuthCookies.userAuth.token &&
                <ModalForAddUser
                    onClose={onCloseModalAddUser}
                    token={userAuthCookies.userAuth.token ?? currentEditor.token}
                />
            }

            <div className={WR_S.menu}>

                <div className={WR_S.logout}
                     onClick={() => unLogin()}>
                    Выйти
                </div>

                <div className={(userAuthCookies.userAuth && userAuthCookies.userAuth.role === role.simple)
                    || (currentEditor && currentEditor.role === role.simple)
                    ? WR_S.Admin_Profile_disabled : WR_S.Admin_Profile}
                    onClick={() => setCurrentAdminProfileEdit()}>
                    Профиль
                </div>

            </div>

            {currentEditor && currentEditor.role === role.admin &&
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

                        <button className={WR_S.add_user_button} onClick={() => setAddUserIsActive(true)}>add user</button>

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
                                        <button className={WR_S.Edit_Button}
                                                onClick={() => setIsEditing(
                                                    {
                                                        isEditing: true,
                                                        uid: element.uid
                                                    }
                                                    )}><img src={pen} alt="Edit information"/>
                                        </button>
                                        <button className={WR_S.Delete_Button} onClick={() => setIsEditing({
                                            isEditing: false,
                                            uid: element.uid
                                        })}><img src={delete_user} alt="Delete user"/>
                                        </button>
                                    </div>
                                </div>)
                            )}
                        </div>
                    </div>
                </div>}

            {/*simple and admin editing*/}
            {(adminUserEdit || currentEditor) && isEditing && isEditing.isEditing && editedUser && <div className={WR_S.Admin_UseProfile}>

                {currentEditor.role === role.admin &&
                    <button onClick={() => switchEditMode()} className={WR_S.Group_user_button}>
                        edit group of this user
                    </button>
                }

                <ProfileView data={editedUser}/>

                {!isEditingGroup && <UserEditForm userData={editedUser} onUserDataChange={handleUserDataChange}
                               fieldIsChange={isFieldChanged}
                               role={currentEditor.role ?? userAuthCookies['userAuth'].role}/>}

                {isEditingGroup && <UserGroupForm userData={
                    {
                        cn: 'test cn',
                        dn: 'test dn',
                        gidNumber: 100,
                        objectClass: ['testOb1','testOb2'],
                        memberUid: 'testmeber uid',
                    }
                } />}
            </div>}

            {currentEditor && isEditing && isEditing.isEditing && editedUser && <div className={WR_S.button_group}>
                <button className={WR_S.submitButton}
                        onClick={() => saveChanges()}>
                    сохранить изменения
                </button>

                <button className={WR_S.cancelChanges}
                        onClick={() => discardChanges()}>
                    сбросить изменения
                </button>

                <button className={WR_S.cancelChanges}
                        onClick={() => {
                            (currentEditor.role === role.simple) ?
                                quitForSimpleUser() : quitForAdmin()
                        }}>
                    выйти к {currentEditor.role === role.admin ?
                    <span>списку</span> : <span>авторизации</span>}
                </button>
            </div>}
        </div>
    </>)
}

export default WorkRoom;
