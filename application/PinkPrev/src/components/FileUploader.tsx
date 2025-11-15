import { useCallback, useState } from 'react'
import { useDropzone } from 'react-dropzone'
import { DragDropBox } from './styles/FloatingBox.style'

import InputLabel from '@mui/material/InputLabel'
import MenuItem from '@mui/material/MenuItem'
import { type SelectChangeEvent } from '@mui/material/Select'

import { FittedImage } from './styles/Image.style'
import { ButtonStyle } from './styles/CustomiseMui.style'
import axios from 'axios'
import { CustomSelect } from './styles/CustomSelect.styled'

import Dialog from '@mui/material/Dialog'
import DialogTitle from '@mui/material/DialogTitle'
import DialogContent from '@mui/material/DialogContent'
import DialogContentText from '@mui/material/DialogContentText'
import DialogActions from '@mui/material/DialogActions'
import Button from '@mui/material/Button'

type PinkPrevFormProps = {
    setResult: (res: string) => void;
}

export default function PinkPrevForm({ setResult }: PinkPrevFormProps) {
    const viewSelection = ["", "CC", "MLO"]
    const sideSelection = ["", "Left", "Right"]

    const [selectedView, setSelectedView] = useState<string>("")
    const [selectedSide, setSelectedSide] = useState<string>("")
    const [preview, setPreview] = useState<string | ArrayBuffer | null>(null)
    const [errorMessage, setErrorMessage] = useState<string>("")
    const [isModalOpen, setModalOpen] = useState<boolean>(false)

    const handleViewChange = (event: SelectChangeEvent<string>) => {
        setSelectedView(event.target.value)
    }

    const handleSideChange = (event: SelectChangeEvent<string>) => {
        setSelectedSide(event.target.value)
    }

    const onDrop = useCallback((acceptedFiles: File[]) => {
        const file = new FileReader()
        file.onload = () => {
            setPreview(file.result)
        }
        file.readAsDataURL(acceptedFiles[0])
    }, [])

    const { acceptedFiles, getRootProps, getInputProps, isDragActive } = useDropzone({
        onDrop,
        accept: {
            'image/jpeg': ['.jpeg', '.jpg'],
            'image/png': ['.png']
        }
    })

    const validateForm = () => {
        if (!selectedSide || !selectedView || typeof acceptedFiles[0] === 'undefined') {
            let error = ""
            if (!selectedSide) error += "- Please select a side.\n"
            if (!selectedView) error += "- Please select a view.\n"
            if (!acceptedFiles[0]) error += "- Please upload an image.\n"
            setErrorMessage(error.trim())
            setModalOpen(true)
            return false
        }
        return true
    }

    const handleCloseModal = () => setModalOpen(false)

    async function handleOnSubmit(e: React.SyntheticEvent) {
        e.preventDefault()

        if (!validateForm()) return

        const formData = new FormData()
        formData.append('file', acceptedFiles[0])
        formData.append('side', selectedSide)
        formData.append('view', selectedView)

        try {
            const response = await axios.post(
                'http://127.0.0.1:5000/api/mamogram',
                formData,
                {
                    headers: {
                        'Content-Type': 'multipart/form-data',
                    },
                }
            )
            setResult(JSON.stringify(response.data))
        } catch (error) {
            console.error('Upload error:', error)
            setResult('Error while uploading.')
        }
    }

    return (
        <div>
            <form onSubmit={handleOnSubmit}>
                <InputLabel id="side-label">Side:</InputLabel>
                <CustomSelect
                    value={selectedSide}
                    label="Side"
                    onChange={handleSideChange}
                >
                    <MenuItem value="" disabled>Select the side</MenuItem>
                    {sideSelection.slice(1).map((item, index) => (
                        <MenuItem key={index} value={item}>
                            {item}
                        </MenuItem>
                    ))}
                </CustomSelect>

                <InputLabel id="view-label">View:</InputLabel>
                <CustomSelect
                    value={selectedView}
                    label="View"
                    onChange={handleViewChange}
                >
                    <MenuItem value="" disabled>Select view</MenuItem>
                    {viewSelection.slice(1).map((item, index) => (
                        <MenuItem key={index} value={item}>
                            {item}
                        </MenuItem>
                    ))}
                </CustomSelect>

                <InputLabel id="picture-label">Picture:</InputLabel>
                <div {...getRootProps()}>
                    <DragDropBox>
                        <input {...getInputProps()} />
                        {
                            typeof preview === "string" ?
                                <FittedImage src={preview} />
                                :
                                isDragActive
                                    ? <p>Drop the picture here ...</p>
                                    : <p>Drag and drop the mammography here ...</p>
                        }
                    </DragDropBox>
                </div>

                <ButtonStyle type="submit" variant="contained" size="large">
                    Send data
                </ButtonStyle>
            </form>

            <Dialog open={isModalOpen} onClose={handleCloseModal}>
                <DialogTitle>Form Error</DialogTitle>
                <DialogContent>
                    <DialogContentText component="pre" style={{ whiteSpace: 'pre-wrap' }}>
                        {errorMessage}
                    </DialogContentText>
                </DialogContent>
                <DialogActions>
                    <Button onClick={handleCloseModal} autoFocus>
                        OK
                    </Button>
                </DialogActions>
            </Dialog>
        </div>
    )
}
