import {Params} from "@/components/pages/workroom/workRoom";
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
