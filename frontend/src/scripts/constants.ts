import {UserRole} from "@/components/pages/workroom/workRoom";

export const homeUrl: string = 'http://172.16.1.63:8081'
export const domain: string = `${homeUrl}/api/v1/`
export const APIS = {
    API : `${domain}api/v1/`,
    GROUPS : `${domain}groups/posixgroup/`,
    USERS : `${domain}users`,
    U_ME : `${domain}users/me/`,
    AUTH : `${domain}auth/token`,
    FILES : `${domain}files`
}

export const gRole: UserRole = {
    admin: 'webadmin',
    simple: 'simpleuser',
}
