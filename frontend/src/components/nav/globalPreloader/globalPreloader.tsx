import GP_S from "@/components/nav/globalPreloader/globalPreloader.module.scss"
const GlobalPreloader: React.FC = () => {
    return (<>
        <div className={GP_S.window}>
            <div className={GP_S.preloaderBlock}>
                <span className={GP_S.preloaderText}></span>
                <div className={GP_S.sliderBlock}>
                    <div className={GP_S.slider}></div>
                </div>
            </div>
        </div>
    </>)
}
export default GlobalPreloader;
