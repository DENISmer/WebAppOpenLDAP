import FFE_S from "@/components/pages/workroom/editor/userEditor/formForEdit.module.scss"
import expand_more from "@/assets/icons/expand_more.png";
import add_object from "@/assets/icons/add_item_v2.svg";
import {userGroupDataForEdit} from "@/components/pages/workroom/workRoom";

interface Props {
    userData: userGroupDataForEdit
}
export const UserGroupForm: React.FC<Props> = ({userData}) => {


    return (<>
        <form className={FFE_S.Admin_form_for_groups}>
            <div className={FFE_S.public_div}>
                <input type="text" value={userData.cn}/>
            </div>
            <div className={FFE_S.public_div}>
                <input type="text" value={userData.gidNumber}/>
            </div>
            <div className={FFE_S.public_div}>
                <input type="text" value={userData.dn}/>
            </div>
            <div className={FFE_S.public_div}>
                <input type="text" value={userData.objectClass[0] ?? 'hellew'}/>
            </div>
            <div className={FFE_S.public_div}>
                <input type="text" value={userData.memberUid}/>
            </div>
        </form>
    </>)
}
