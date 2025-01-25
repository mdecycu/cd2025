<?xml version="1.0" encoding="utf-8"?>
<!-- Created by Leo: https://leo-editor.github.io/leo-editor/leo_toc.html -->
<leo_file xmlns:leo="https://leo-editor.github.io/leo-editor/namespaces/leo-python-editor/1.1" >
<leo_header file_format="2"/>
<globals/>
<preferences/>
<find_panel_settings/>
<vnodes>
<v t="leo.20250125233710.2"><vh>original onlink_leo2.wbt</vh></v>
<v t="leo.20250125233733.1"><vh>@clean onelink_leo2.wbt</vh>
<v t="leo.20250126000845.1"><vh>#VRML</vh></v>
<v t="leo.20250126051919.1"><vh>EXTERNPROTO</vh></v>
<v t="leo.20250126001100.1"><vh>WorldInfo</vh></v>
<v t="leo.20250126052014.1"><vh>Viewpoint</vh>
<v t="leo.20250126053237.1"><vh>orientation</vh></v>
<v t="leo.20250126053300.1"><vh>position</vh></v>
</v>
<v t="leo.20250126052035.1"><vh>TextureBackground</vh></v>
<v t="leo.20250126052058.1"><vh>TextureBackgroundLight</vh></v>
<v t="leo.20250126052115.1"><vh>RectangleArena</vh></v>
<v t="leo.20250126001114.1"><vh>Robot</vh>
<v t="leo.20250126001233.1"><vh>children</vh>
<v t="leo.20250126052149.1"><vh>Solid</vh>
<v t="leo.20250126052212.1"><vh>children</vh>
<v t="leo.20250126052234.1"><vh>BaseSolid</vh></v>
<v t="leo.20250126052300.1"><vh>HingeJoint</vh>
<v t="leo.20250126052331.1"><vh>jointParameters</vh>
<v t="leo.20250126053351.1"><vh>axis</vh></v>
</v>
<v t="leo.20250126052408.1"><vh>device</vh>
<v t="leo.20250126052511.1"><vh>RotationalMotor</vh>
<v t="leo.20250126053117.1"><vh>name</vh></v>
</v>
</v>
<v t="leo.20250126052433.1"><vh>endPoint Solid</vh>
<v t="leo.20250126052552.1"><vh>children</vh>
<v t="leo.20250126064827.1"><vh>JointSolid</vh></v>
<v t="leo.20250126064900.1"><vh>Solid</vh>
<v t="leo.20250126064927.1"><vh>translation</vh></v>
<v t="leo.20250126064952.1"><vh>children</vh>
<v t="leo.20250126065046.1"><vh>LinkSolid</vh></v>
<v t="leo.20250126065112.1"><vh>Solid</vh>
<v t="leo.20250126065131.1"><vh>translation</vh></v>
<v t="leo.20250126065145.1"><vh>children</vh>
<v t="leo.20250126065230.1"><vh>HingeJoint</vh>
<v t="leo.20250126065327.1"><vh>jointParameters</vh></v>
<v t="leo.20250126065353.1"><vh>device</vh>
<v t="leo.20250126065758.1"><vh>RotationalMotor</vh>
<v t="leo.20250126065825.1"><vh>name</vh></v>
<v t="leo.20250126070737.1"><vh>maxVelocity</vh></v>
</v>
</v>
<v t="leo.20250126065407.1"><vh>endPoint Solid</vh>
<v t="leo.20250126065436.1"><vh>children</vh>
<v t="leo.20250126065500.1"><vh>JointSolid</vh></v>
<v t="leo.20250126065519.1"><vh>Solid</vh>
<v t="leo.20250126065541.1"><vh>children</vh>
<v t="leo.20250126065606.1"><vh>LinkSolid</vh></v>
</v>
</v>
</v>
</v>
</v>
</v>
</v>
</v>
</v>
</v>
</v>
</v>
</v>
</v>
</v>
<v t="leo.20250126001238.1"><vh>controller</vh></v>
</v>
</v>
<v t="leo.20250126055419.1"><vh>@path ./../controllers/joint_controller</vh>
<v t="leo.20250126055419.2"><vh>@auto joint_controller.py</vh></v>
</v>
<v t="leo.20250125235802.1"><vh>@path ./../controllers/joint_controller2</vh>
<v t="leo.20250125235721.1"><vh>@edit joint_controller2.py</vh></v>
</v>
</vnodes>
<tnodes>
<t tx="leo.20250125233710.2">#VRML_SIM R2023b utf8
EXTERNPROTO "../protos/TexturedBackground.proto"
EXTERNPROTO "../protos/TexturedBackgroundLight.proto"
EXTERNPROTO "../protos/RectangleArena.proto"
EXTERNPROTO "../protos/BaseSolid.proto"
EXTERNPROTO "../protos/JointSolid.proto"
EXTERNPROTO "../protos/LinkSolid.proto"
WorldInfo {}
Viewpoint {
    orientation -0.17911760145636924 0.20303955404969007 0.9626483388755317 1.7931226479511868
    position 0.7495096875887461 -3.1141998018989674 1.7796380905257032
}
TexturedBackground {}
TexturedBackgroundLight {}
RectangleArena {}
Robot {
    children [
        Solid {
            children [
                BaseSolid { }  # 基座
                HingeJoint {
                    jointParameters HingeJointParameters {
                        axis 0 0 1
                    }
                    device [
                        RotationalMotor {
                            name "joint_motor"
                        }
                    ]
                    endPoint Solid {
                        children [
                            JointSolid { }  # 第一個關節
                            Solid {
                                translation 0 0 0
                                children [
                                    LinkSolid { }  # 第一個連桿
                                    Solid {
                                        #translation 1-0.125 0 0.15
                                        translation 0.875 0 0.15
                                        children [
                                            HingeJoint {
                                                jointParameters HingeJointParameters {
                                                    axis 0 0 1
                                                }
                                                device [
                                                    RotationalMotor {
                                                        name "joint_motor2"
                                                    }
                                                ]
                                                endPoint Solid {
                                                    children [
                                                        JointSolid { }  # 第二個關節
                                                        Solid {
                                                            children [
                                                                LinkSolid { }  # 第二個連桿
                                                            ]
                                                        }
                                                    ]
                                                }
                                            }
                                        ]
                                    }
                                ]
                            }
                        ]
                    }
                }
            ]
        }
    ]
    controller "joint_controller2"
}</t>
<t tx="leo.20250125233733.1">@others
</t>
<t tx="leo.20250125235802.1"></t>
<t tx="leo.20250126000845.1">#VRML_SIM R2023b utf8
</t>
<t tx="leo.20250126001100.1">WorldInfo {}
</t>
<t tx="leo.20250126001114.1">Robot {
    @others
}
</t>
<t tx="leo.20250126001233.1">children [
    @others
]
</t>
<t tx="leo.20250126001238.1">controller "joint_controller2"
</t>
<t tx="leo.20250126051919.1">EXTERNPROTO "../protos/TexturedBackground.proto"
EXTERNPROTO "../protos/TexturedBackgroundLight.proto"
EXTERNPROTO "../protos/RectangleArena.proto"
EXTERNPROTO "../protos/BaseSolid.proto"
EXTERNPROTO "../protos/JointSolid.proto"
EXTERNPROTO "../protos/LinkSolid.proto"
</t>
<t tx="leo.20250126052014.1">Viewpoint {
    @others
}
</t>
<t tx="leo.20250126052035.1">TexturedBackground {}
</t>
<t tx="leo.20250126052058.1">TexturedBackgroundLight {}
</t>
<t tx="leo.20250126052115.1">RectangleArena {}
</t>
<t tx="leo.20250126052149.1">Solid {
    @others
}
</t>
<t tx="leo.20250126052212.1">children [
    @others
]
</t>
<t tx="leo.20250126052234.1">BaseSolid { }  # 基座
</t>
<t tx="leo.20250126052300.1">HingeJoint {
    @others
}
</t>
<t tx="leo.20250126052331.1">jointParameters HingeJointParameters {
    @others
}
</t>
<t tx="leo.20250126052408.1">device [
    @others
]
</t>
<t tx="leo.20250126052433.1">endPoint Solid {
    @others
}
</t>
<t tx="leo.20250126052511.1">RotationalMotor {
    @others
}
</t>
<t tx="leo.20250126052552.1">children [
    @others
]
</t>
<t tx="leo.20250126053117.1">name "joint_motor"
</t>
<t tx="leo.20250126053237.1">orientation -0.17911760145636924 0.20303955404969007 0.9626483388755317 1.7931226479511868
</t>
<t tx="leo.20250126053300.1">position 0.7495096875887461 -3.1141998018989674 1.7796380905257032
</t>
<t tx="leo.20250126053351.1">axis 0 0 1
springConstant 0
dampingConstant 0
</t>
<t tx="leo.20250126055419.1"></t>
<t tx="leo.20250126064827.1">JointSolid { }  # 第一個關節
</t>
<t tx="leo.20250126064900.1">Solid {
    @others
}</t>
<t tx="leo.20250126064927.1">translation 0 0 0
</t>
<t tx="leo.20250126064952.1">children [
    @others
]</t>
<t tx="leo.20250126065046.1">LinkSolid { }  # 第一個連桿</t>
<t tx="leo.20250126065112.1">Solid {
    @others
}</t>
<t tx="leo.20250126065131.1">#translation 1-0.125 0 0.15
translation 0.875 0 0.15
</t>
<t tx="leo.20250126065145.1">children [
    @others
]</t>
<t tx="leo.20250126065230.1">HingeJoint {
    @others
}</t>
<t tx="leo.20250126065327.1">jointParameters HingeJointParameters {
    axis 0 0 1
    springConstant 0 
    dampingConstant 0
}
</t>
<t tx="leo.20250126065353.1">device [
    @others
]
</t>
<t tx="leo.20250126065407.1">endPoint Solid {
    @others
}</t>
<t tx="leo.20250126065436.1">children [
    @others
]</t>
<t tx="leo.20250126065500.1">JointSolid { }  # 第二個關節
</t>
<t tx="leo.20250126065519.1">Solid {
    @others
}</t>
<t tx="leo.20250126065541.1">children [
    @others
]</t>
<t tx="leo.20250126065606.1">LinkSolid { }  # 第二個連桿</t>
<t tx="leo.20250126065758.1">RotationalMotor {
    @others
}</t>
<t tx="leo.20250126065825.1">name "joint_motor2"</t>
<t tx="leo.20250126070737.1">maxVelocity 100.0  # 添加最大速度限制</t>
</tnodes>
</leo_file>
