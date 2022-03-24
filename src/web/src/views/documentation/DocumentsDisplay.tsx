import * as React from 'react';
import { Box,  Drawer, Toolbar, Container } from '@mui/material';
import axios from 'axios';
import ReactMarkdown from 'react-markdown'
import gfm from 'remark-gfm'


import { useParams } from 'react-router';
import DocumentsTree, { DecodeResponseDocumentTreeNode, DocumentTreeNode, ResponseDocumentTreeNode } from './DocumentsTree';

const drawerWidth = 300;

function DocumentsDisplay(props: {
    params: {
        docId?: string
    }
}) {
    const [selected, setSelected] = React.useState<string | undefined>(undefined);
    const [documentTree, setDocumentTree] = React.useState<DocumentTreeNode[]>([]);
    const [markDownContent, setMarkDownContent] = React.useState<string | undefined>(undefined);

    const loadDocumentIndex = () => {
        axios.get('/Docs/Index')
            .then(res => {
                const pages: ResponseDocumentTreeNode[] = res.data;
                const documentTree: DocumentTreeNode[] = pages.map(e => DecodeResponseDocumentTreeNode(e));
                setDocumentTree(documentTree);
            }).catch(err => console.error(err.response));
    }

    const loadDocument = (nodeId: string) => {
        axios.get(`/Docs/Index/${nodeId}`)
            .then(res => {
                if (res.status === 204) {
                    return
                }
                const content = res.data;
                setMarkDownContent(content);
            }).catch(err => console.error(err.response));
    }

    const handleTreeSelect = (nodeId: string) => {
        setSelected(nodeId);
        loadDocument(nodeId);
    }

    React.useEffect(() => {
        if (props.params.docId) {
            handleTreeSelect(props.params.docId);
        }
    }, [props.params.docId])

    React.useEffect(() => {
        loadDocumentIndex();
    }, [])

    return (
        <React.Fragment>
            <Box sx={{ display: 'flex' }}>
                <Drawer
                    variant="permanent"
                    sx={{
                        width: drawerWidth,
                        flexShrink: 0,
                        [`& .MuiDrawer-paper`]: { width: drawerWidth, boxSizing: 'border-box' },
                        zIndex: (theme) => theme.zIndex.appBar - 1
                    }}
                >
                    <Toolbar />
                    {selected && documentTree.length > 0 && <DocumentsTree
                        nodes={documentTree}
                        selected={selected}
                        onSelected={handleTreeSelect}
                    />}
                </Drawer>

                <Container sx={{
                    flexGrow: 1,
                }}>
                    <Toolbar sx={{ flexShrink: 0 }} />
                    <Box sx={{ pt: 2 }}>
                        {markDownContent && <ReactMarkdown
                            remarkPlugins={[gfm]}
                            children={markDownContent}
                        />}
                    </Box>
                </Container>
            </Box>
        </React.Fragment>
    )
}

const DocumentsDisplayWrapper = (props: any) => {
    const params = useParams()
    return <DocumentsDisplay params={params} {...props} />
}

export { DocumentsDisplayWrapper as DocumentsDisplay };
