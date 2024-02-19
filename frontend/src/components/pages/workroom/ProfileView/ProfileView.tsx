import PV_S from "@/components/pages/workroom/ProfileView/ProfileView.module.scss"
export function ProfileView(){
    return (
        <div className={PV_S.Profile_Module}>
            this is all profile block
            <div className={PV_S.Profile_Body}>
                profile body
                <div className={PV_S.Profile_Content}>
                    content here
                    <div>photo</div>
                    <p>John Swan</p>
                    <p>uid=john,ou=people,dc=example,dc=com</p>
                    <p>john@mail.ru</p>
                    <p>display name</p>
                    <p>inetOrgPerson</p>
                    <p>loginShell</p>
                    <p>postalCode</p>
                </div>
            </div>
        </div>
    )
}
