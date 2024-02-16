import React from "react";
import MW_S from "@/components/Modal_Window/modal_window_style.module.scss"

interface Props {
    active: boolean;
    text: string;
    modal: (active: boolean, data: string) => void;
}
export const Modal = (data: Props | null) => {

    //const [modalView, setModalView] = useState<Props>(null);


    return(<>
            <div className={data.active ? `${MW_S.modal} ${MW_S.modal_active}` : MW_S.modal} onClick={() => data.modal(data.active, null)}>
                <div className={data.active ? `${MW_S.modal__content} ${MW_S.modal__content_active}` : MW_S.modal__content} onClick={(e) => e.stopPropagation()}>
                    <span className={MW_S.text}>{data.text}</span>
                </div>
            </div>
        </>
    )
}

