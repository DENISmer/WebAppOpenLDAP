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

export async function getUserDataByUid_Admin(props: string): Promise<userDataForEdit> {
    console.log(props)
    const request = axios.get(`${APIS.USERS}/${props}`, {
        headers: {
            Authorization: `Bearer ${props}`
        },
    }).then((response) => {
        return response.data
    }).catch((e) => {
        console.log(e.message)
    })

    return request
}

async function sendChanges(data: userDataForEdit){
    return axios.patch(`${APIS.USERS}`)
}

export function validateChanges(data: userDataForEdit){
    for (let key in data){
        if(key === 'uid' || 'gid'){
            Number(data[key])
        }
        if(!data[key] || data[key].length < 1){
            return 0
        }
        else return data
    }
}
