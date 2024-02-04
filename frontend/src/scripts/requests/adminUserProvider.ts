import {Params} from "@/components/pages/workroom/workRoom";
import axios from "axios";
import {APIS} from "@/scripts/constants";

export async function getUsersList(props: Params) {
    console.log(props.token)
    const request = axios.get(APIS.USERS,{
        headers: {
            Authorization: `Bearer ${props.token}`
        }
    })
        .then((response) => {
           console.log(response)
        })
        .catch((e) => {
            console.log(e.message)
        })

    console.log(request)

}