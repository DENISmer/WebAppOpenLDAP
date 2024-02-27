import {Params, userDataForEdit, userGroupDataForEdit} from "@/components/pages/workroom/workRoom";
import axios from "axios";
import {APIS} from "@/scripts/constants";

export interface ReturnThenPatch {
    userData?: userDataForEdit,
    status: number
}

export interface PatchParams {
    userData: userDataForEdit,
    currentToken: string
}

export interface userAddDataForEdit {
    photoUrl? : string,
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
    objectClass: string[],
    userPassword: string
}

export interface getUserGroupData {
    token: string,
    role?: string,
    uid: string,
}
export interface ErrorData {
    message: string,
    status: number
}

export async function getUsersList(props: Params) {
    console.log(props.token)
    return await axios.get(`${APIS.USERS}?search=${props.value}&page=${props.pageNumber}`,{
        headers: {
            Authorization: `Bearer ${props.token}`
        },
    }
    ).then((response) => {
           return response
        })
        .catch((e) => {
            return e
        })
}

export async function getUserDataByUid_Admin(props: string, Params): Promise<userDataForEdit> {
    console.log(Params.token)
    return await axios.get(`${APIS.USERS}/${props}`, {
        headers: {
            Authorization: `Bearer ${Params.token}`
        },
    }).then((response) => {
        //console.log(response,'anywayh')
        return response.data
    }).catch((e: any) => {
        return {error: e.response}
    })
}

export async function sendChanges(data: PatchParams['userData'], token: string, role: string, uid: string): Promise<ReturnThenPatch> {
    if (role === 'simple_user'){
        return await axios.patch(`${APIS.USERS}/${uid}`,{
            mail: data.mail,
        }, {
            headers: {
                Authorization: `Bearer ${token}`
            }
        })
            .then((response) => {
                if(response.request.status === 200){
                    return {userData :response.data, status: response.request.status }
                }
            })
            .catch((e) => {
                return e.response.data
            })
    } else return await axios.patch(`${APIS.USERS}/${uid}`,{
        uidNumber: data.uidNumber,
        gidNumber: data.gidNumber,
        uid: data.uid,
        sshPublicKey: data.sshPublicKey,
        st: data.st,
        mail: data.mail,
        street: data.street,
        cn: data.cn,
        displayName: data.displayName,
        givenName: data.givenName,
        sn: data.sn,
        postalCode: data.postalCode,
        homeDirectory: data.homeDirectory,
        loginShell: data.loginShell,
        objectClass: data.objectClass
    }, {
        headers: {
            Authorization: `Bearer ${token}`
        }
    })
        .then((response) => {
            if(response.request.status === 200){
                return {userData :response.data, status: response.request.status }
            }
        })
        .catch((e) => {
            return e.response.data
        })
}

export async function deleteUser(uid: string,token: string) {
    if(uid){
        return await axios.delete(`${APIS.USERS}/${uid}`,{
            headers: {
                Authorization: `Bearer ${token}`
            }
        })
            .then((response) => {
                return response
            })
            .catch((e) => {
                alert(`smth went wrong ${e}`)
            })
    }
}

export async function addUser(data: userAddDataForEdit, token: string): Promise<userGroupDataForEdit | ErrorData> {
    console.log("REQuest data: ",data)
    return await axios.post(`${APIS.USERS}`,
        {
            dn: data.dn,
            uid: data.uid,
            sshPublicKey: data.sshPublicKey,
            st: data.st,
            mail: data.mail,
            street: data.street,
            cn: data.cn,
            displayName: data.displayName,
            givenName: data.givenName,
            sn: data.sn,
            postalCode: data.postalCode,
            homeDirectory: data.homeDirectory,
            loginShell: data.loginShell,
            objectClass: data.objectClass,
            userPassword: data.userPassword
        },
        {
            headers: {
                Authorization: `Bearer ${token}`
            }
        }
        )
        .then((response): userGroupDataForEdit => {
            alert("Данные успешно сохранены")
            return response.data
        })
        .catch((e): ErrorData  => {
            return e.response.data
        })
}

export async function getUserGroupData(data: getUserGroupData): Promise<userGroupDataForEdit | ErrorData> {
    return await axios.get(`${APIS.GROUPS}${data.uid}`,{
        headers: {
            Authorization: `Bearer ${data.token}`,
        }
    })
        .then((response): userGroupDataForEdit => {
            return response.data
        })
        .catch((e): ErrorData => {
            return e.response.data
        })
}

