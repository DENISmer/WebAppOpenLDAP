import PV_S from "@/components/pages/workroom/ProfileView/ProfileView.module.scss"
import {userDataForEdit} from "@/components/pages/workroom/workRoom";

interface Props {
    data: userDataForEdit
}

export const ProfileView: React.FC<Props> = ({data}) => {
    return (
        <div className={PV_S.Profile_Module}>
            <div className={PV_S.Profile_Body}>
                <div className={PV_S.Profile_Content}>
                    <div>
                        <img src="https://www.dpstudio.ru/PhotoExaples/Visa_USA_0.jpg" alt=""/>
                    </div>
                    <p>{data.displayName ?? data.uid}</p>
                    <p>{data.dn}</p>
                    <p>{data.uidNumber}</p>
                    {data.mail && data.mail.length > 0 && <p>{data.mail && data.mail[0]}</p>}
                    <p>{data.homeDirectory}</p>
                    {data.street && <p>{data.street}</p>}
                    {data.postalCode && <p>{data.postalCode}</p>}
                </div>
            </div>
        </div>
    )
}
