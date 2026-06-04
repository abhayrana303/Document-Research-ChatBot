import React, { useState, useRef } from 'react';

/**
 * DocumentUploader — handles file selection (click or drag-and-drop) and upload.
 * Props:
 *   onUpload : function — called after a successful upload to refresh the document list
 */
const DocumentUploader = ({ onUpload }) => {
    const [selectedFiles, setSelectedFiles] = useState(null);
    const [uploadStatus, setUploadStatus] = useState('');
    const [isUploading, setIsUploading] = useState(false);
    const [isDragging, setIsDragging] = useState(false);
    const fileInputRef = useRef(null);

    const applyFiles = (files) => {
        if (files && files.length > 0) {
            setSelectedFiles(files);
            setUploadStatus('');
        }
    };

    const handleFileChange = (event) => {
        applyFiles(event.target.files);
    };

    // ── Drag-and-drop handlers ──────────────────────────
    const handleDragOver = (e) => {
        e.preventDefault();
        e.stopPropagation();
        setIsDragging(true);
    };

    const handleDragLeave = (e) => {
        e.preventDefault();
        e.stopPropagation();
        setIsDragging(false);
    };

    const handleDrop = (e) => {
        e.preventDefault();
        e.stopPropagation();
        setIsDragging(false);
        applyFiles(e.dataTransfer.files);
    };

    // ── Upload handler ──────────────────────────────────
    const handleUpload = async () => {
        if (!selectedFiles || selectedFiles.length === 0) {
            setUploadStatus('Please select or drop files to upload.');
            return;
        }
        setIsUploading(true);
        setUploadStatus('Uploading...');

        const formData = new FormData();
        for (let i = 0; i < selectedFiles.length; i++) {
            formData.append('files', selectedFiles[i]);
        }

        try {
            const response = await fetch('/upload/', {
                method: 'POST',
                body: formData,
            });
            const data = await response.json();

            if (response.ok) {
                setUploadStatus(`✅ ${data.message} (${data.ids.join(', ')})`);
                // Reset file input and state after successful upload
                setSelectedFiles(null);
                if (fileInputRef.current) fileInputRef.current.value = '';
                if (onUpload) onUpload();
            } else {
                setUploadStatus(`❌ Failed: ${data.error || 'Unknown error'}`);
            }
        } catch (error) {
            setUploadStatus('❌ Network error — is the backend running?');
        } finally {
            setIsUploading(false);
        }
    };

    const fileLabel = selectedFiles
        ? `${selectedFiles.length} file${selectedFiles.length !== 1 ? 's' : ''} selected`
        : 'Click to browse or drag & drop files here';

    return (
        <div
            className={`document-uploader ${isDragging ? 'dragging' : ''}`}
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
        >
            {/* Hidden native file input, triggered by the label click */}
            <input
                ref={fileInputRef}
                type="file"
                multiple
                accept=".pdf,.txt,.png,.jpg,.jpeg,.bmp"
                onChange={handleFileChange}
                id="file-input"
                style={{ display: 'none' }}
            />

            <div className="uploader-body">
                <div className="upload-icon">📂</div>
                <label htmlFor="file-input" className="upload-label">
                    {fileLabel}
                </label>
                <p className="upload-hint">Supported: PDF, TXT, PNG, JPG, BMP</p>
            </div>

            <button
                className="btn btn-primary"
                onClick={handleUpload}
                disabled={isUploading || !selectedFiles}
            >
                {isUploading ? '⏳ Uploading...' : '⬆ Upload Documents'}
            </button>

            {uploadStatus && (
                <p className={uploadStatus.startsWith('❌') ? 'status-error' : 'status-success'}>
                    {uploadStatus}
                </p>
            )}
        </div>
    );
};

export default DocumentUploader;