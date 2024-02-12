import {Params, userDataForEdit} from "@/components/pages/workroom/workRoom";
import axios from "axios";
import {APIS} from "@/scripts/constants";
import {response} from "express";

export interface ReturnThenPatch {
    userData?: userDataForEdit,
    status: number
}

export interface PatchParams {
    userData: userDataForEdit,
    currentToken: string
}

export async function getUsersList(props: Params) {
    console.log(props.token)
    const request = axios.get(`${APIS.USERS}?search=${props.value}&page=${props.pageNumber}`,{
        headers: {
            Authorization: `Bearer ${props.token}`
        },
    }
    ).then((response) => {
           return response
        })
        .catch((e) => {
            e.response
        })
    return request
}

export async function getUserDataByUid_Admin(props: string, Params): Promise<userDataForEdit> {
    console.log(Params.token)
    const request = axios.get(`${APIS.USERS}/${props}`, {
        headers: {
            Authorization: `Bearer ${Params.token}`
        },
    }).then((response) => {
        return response.data
    }).catch((e) => {
        console.log(e.message)
    })

    return request
}

export async function sendChanges(data: PatchParams['userData'], token: PatchParams['currentToken']): Promise<ReturnThenPatch> {
    //console.log(data)
    const sendDataToChange = await axios.patch(`${APIS.USERS}/${data.uid}`,{
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
            console.log('FterReq',response)
            if(response.request.status === 200){
                return {userData :response.data, status: response.request.status }
            }
        })
        .catch((e) => {
            console.log("E", e.response.data)
            return e.response.data
        })

    return  sendDataToChange
}

export async function deleteUser(uid: string) {
    if(uid){
        return await axios.delete(`${APIS.USERS}/${uid}`,{
            headers: {
                Authorization: `Bearer ${uid}`
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

