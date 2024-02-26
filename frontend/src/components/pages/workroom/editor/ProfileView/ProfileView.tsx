import PV_S from "@/components/pages/workroom/editor/ProfileView/ProfileView.module.scss"
import {userDataForEdit} from "@/components/pages/workroom/workRoom";
import axios from "axios";
import {APIS} from "@/scripts/constants";
import {useCookies} from "react-cookie";
import {useEffect, useState} from "react";

interface Props {
    data: userDataForEdit
}

export const ProfileView: React.FC<Props> = ({data}) => {
    const [userAuthCookies, setUserAuthCookie, removeCookie] = useCookies(['userAuth', 'userAttempt'])

    const [file, setFile] = useState<File | null>(null);
    const [jsonData, setJsonData] = useState<object>({dn: 'asd', sn: 'sn'});

    const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        if (event.target.files && event.target.files.length > 0) {
            setFile(event.target.files[0]);
        }
        // return handleSubmit()
        //     .then((response) => {
        //         console.log(response)
        //     })
        //     .catch((e) => {
        //         console.log(e)
        //     })
    };

    const handleJsonChange = (event: React.ChangeEvent<HTMLTextAreaElement>) => {
        try {
            const data = JSON.parse(event.target.value);
            setJsonData(data);
        } catch (error) {
            console.error('Invalid JSON format');
        }
    };
    useEffect(() =>{
        handleSubmit()
    },[file])
    const handleSubmit = async () => {
        if (!file) {
            //console.error('Please select a file');
            return;
        }

        try {
            const formData = new FormData();
            formData.append('file', file);
            formData.append('data', JSON.stringify(jsonData));
            //console.log(JSON.stringify(jsonData))

            await axios.post(`${APIS.USERS}`, formData, {
                headers: {
                    Authorization: `Bearer ${userAuthCookies.userAuth.token}`,
                    'Content-Type': 'multipart/form-data',
                },
            });

            //console.log('Data sent successfully');
        } catch (error) {
            console.error('Error while sending data:', error);
        }
    };


    return (
        <div className={PV_S.Profile_Module}>
            <div className={PV_S.Profile_Body}>
                <div className={PV_S.Profile_Content}>
                    <div>
                        <img src="https://abrakadabra.fun/uploads/posts/2021-12/1640528610_2-abrakadabra-fun-p-serii-chelovek-na-avu-2.jpg" alt="картинка профиля"/>
                        {/*<input type={"file"} accept={"image/*"} onChange={handleFileChange}/>*/}
                    </div>
                    <br/>
                    <br/>
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
