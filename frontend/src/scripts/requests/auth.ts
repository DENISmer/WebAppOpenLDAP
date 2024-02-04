
import {APIS} from "@/scripts/constants";
import axios from "axios";
export interface AuthParams {
    userName: string
    password: string
}
export interface UserAuth {
    userName: string,
    token: string,
    role: string
}
async function setAuthToken(params: AuthParams): Promise<UserAuth> {
    if (params.userName && params.password) {
        try {
            const response = await axios.post(APIS.AUTH, {
                "username": params.userName,
                "userPassword": params.password
            });
            if (response.status === 200) {
                return {
                    userName: response.data.uid,
                    token: response.data.token,
                    role: response.data.role
                };
            } else {
                throw new Error('Auth failed with status: ' + response.status);
            }
        } catch (err) {
            // It's better to throw an error rather than console.log it so that it can be caught by the caller.
            throw new Error('Auth request failed: ' + err.message);
        }
    } else {
        // If parameters are not provided, throw an error rather than returning a result with placeholders.
        throw new Error('Username or password is missing');
    }
}
export default setAuthToken
