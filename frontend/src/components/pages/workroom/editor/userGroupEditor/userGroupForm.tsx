// import FFE_S from "@/components/pages/workroom/editor/userEditor/formForEdit.module.scss"
import {userGroupDataForEdit} from "@/components/pages/workroom/workRoom";
import UGF_S from "@/components/pages/workroom/editor/userGroupEditor/UserGroupForm.module.scss"

interface Props {
    userData: userGroupDataForEdit
}
export const UserGroupForm: React.FC<Props> = ({userData}) => {


    return (<>
            <form className={UGF_S.groupForm}>
                <div className={UGF_S.public_div_group}>
                    <div className={UGF_S.element_group}>
                            <label>123</label>
                            <input type="text" value={userData.cn}/>
                    </div>
                    <div className={UGF_S.element_group}>
                            <input type="text" value={userData.gidNumber}/>
                    </div>
                    <div className={UGF_S.element_group}>
                            <input type="text" value={userData.dn}/>
                    </div>
                    <div className={UGF_S.element_group}>
                        <input type="text" value={userData.memberUid}/>
                    </div>

                </div>

            </form>
    </>)
}
