import {Params, userDataForEdit} from "@/components/pages/workroom/workRoom";
import axios from "axios";
import {APIS} from "@/scripts/constants";


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

export async function sendChanges(data: userDataForEdit){
    //console.log(data)
    const sendDataToChange = await axios.patch(`${APIS.USERS}/${data.uid}`,{
        uidNumber: data.uidNumber,
        gidNumber: data.gidNumber,
        uid: data.uid,
        //sshPublicKey: data.sshPublicKey,
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
    })
        .then((response) => {
            return response.data
        })
        .catch((e) => {
            return e
        })

    return  sendDataToChange
}

