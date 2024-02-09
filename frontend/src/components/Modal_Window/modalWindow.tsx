import React, {useState} from "react";
import MW_S from "@/components/Modal_Window/modal_window_style.module.scss"
import IntrinsicAttributes = React.JSX.IntrinsicAttributes;


const Modal: React.FC = () => {

    const [modalView, setModalView] = useState(false);


    return(<>
            <div className={modalView ? `${MW_S.modal} ${MW_S.modal_active}` : MW_S.modal} onClick={()=>setModalView(false)}>
                <div className={modalView ? `${MW_S.modal__content} ${MW_S.modal__content_active}` : MW_S.modal__content} onClick={e => e.stopPropagation()}>
                    <p>test text</p>
                </div>
            </div>
        </>
    )
}

export default Modal
