import { PageWrapper }  from "./styles/PageWrapper.style";
import {  BenignTag, FloatingBox, Instructions, LeftPanel, MalignTag, RightPanel } from "./styles/FloatingBox.style";
import PinkPrevForm from "./FileUploader";
import { useState } from "react";
import type { Result } from "./types/Response";

const MainLayout: React.FC = () => {
    const [result, setResult] = useState<string | null>(null);
    
    let parsedResult: Result | null = null;
    if (result !== null) {
        try {
            parsedResult = JSON.parse(result) as Result;
        } catch (error) {
            console.error("Failed to parse result JSON:", error);
        }
    }
    return (
        <PageWrapper>
            <FloatingBox>
                <LeftPanel>
                    <PinkPrevForm setResult={setResult} />
                </LeftPanel>
                <RightPanel>
                    {
                        result && parsedResult ? (
                            <div>
                                {
                                    parsedResult.prediction === 'benign' ?
                                        <BenignTag>
                                            <p>
                                                Prediction: {parsedResult.prediction}
                                            </p>
                                            <p>
                                                Confidence: {(parsedResult.confidence * 100).toFixed(2)}%
                                            </p>
                                        </ BenignTag>
                                    :
                                        <MalignTag>
                                            <p>
                                                Prediction: {parsedResult.prediction}
                                            </p>
                                            <p>
                                                Confidence: {(parsedResult.confidence * 100).toFixed(2)}%
                                            </p>
                                        </ MalignTag>
                                }
                            </div>
                        ) : (
                            <Instructions>
                                <h3>Instructions:</h3>
                                <ul>
                                    <li>1. Select the side (Left/Right)</li>
                                    <li>2. Upload a .jpg or .png image</li>
                                    <li>3. Select the image view (CC/MLO)</li>
                                    <li>4. Click “Send data”</li>
                                </ul>
                            </Instructions>
                        )
                    }
                </RightPanel>
            </FloatingBox>
        </PageWrapper>
    );
};

export default MainLayout;