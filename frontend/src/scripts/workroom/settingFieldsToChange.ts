
type profileProps = {
    homeDirectory: string,
    sn: string,
    givenName: string,
    cn: string,
    displayName: string,
    mail: string[],
    gidNumber?: string,
    st: string,
    objectClass: string[],
    sshPublicKey: string[],
    street: string,
    uid: number,
    postalCode: string,
    loginShell: string,
    uidNumber?: string
}

const settingFieldsToChange: Function =  (props: profileProps) => {

    let privateMethod = function (props : profileProps){
        const setFields: profileProps = {
            homeDirectory: props.homeDirectory,
            sn: props.sn,
            givenName: props.givenName,
            cn: props.cn,
            displayName: props.displayName,
            mail: props.mail,
            st: props.st,
            objectClass: props.objectClass,
            sshPublicKey: props.sshPublicKey,
            street: props.street,
            uid: props.uid,
            postalCode: props.postalCode,
            loginShell: props.loginShell,
        }
        return setFields
    }

    return {
        publicMethod: function (){
            return privateMethod(props)
        }
    }
}

export default settingFieldsToChange;
